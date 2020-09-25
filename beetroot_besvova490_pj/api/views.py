import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UserSerializer, SubjectSerializer, ScheduleSerializer
from .serializers import user_model, subject_model, scheduling_model


class SubjectViewSet(viewsets.ViewSet):

    def list(self, request):
        subject_list = subject_model.objects.all()
        serializer = SubjectSerializer(subject_list, many=True)
        return Response({'msg': 'Subjects list', 'title': 'About',
            'items': serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = subject_model.objects.all()
        subject = get_object_or_404(queryset, pk=pk)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    def create(self, request):
        request.data['data']['lesson_time'] = []
        request.data['data']['users'] = []
        serializer = SubjectSerializer(data=request.data['data'])
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        data = request.data['data']
        queryset = subject_model.objects.all()
        subject = get_object_or_404(queryset, pk=pk)
        data['users'] = data.get('users', [])
        data['schedule'] = data.get('schedule', [])
        serializer = SubjectSerializer(subject, data=request.data['data'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = subject_model.objects.all()
        subject = get_object_or_404(queryset, pk=pk)
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ViewSet):

    def list(self, request):
        query = request.query_params.get('users', 'all')
        if query == 'teachers':
            queryset = user_model.objects.filter(is_teacher=True)
        elif query == 'students':
            queryset = user_model.objects.filter(is_teacher=False)
        else:
            queryset = user_model.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response({'items':  serializer.data})

    def retrieve(self, request, pk=None):
        query = request.query_params
        queryset = user_model.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        if query and query['action'] == 'follow_user':
            follow_user = get_object_or_404(queryset, pk=query['user_id'])
            if user.is_teacher == follow_user.is_teacher:
                return Response({'msg': 'Teacher can not follow teacher'
                                        'and student can not follow student'},
                                status=status.HTTP_400_BAD_REQUEST)
            user.users.add(follow_user)
            user.save()
            return Response({'msg': 'User followed'}, status=status.HTTP_201_CREATED)
        elif query and query['action'] == 'follow_subject':
            queryset_subject = subject_model.objects.all()
            follow_subject = get_object_or_404(queryset_subject, pk=query['subject_id'])
            if follow_subject in user.subjects.all():
                return Response({'msg': 'User already in subject'},
                                status=status.HTTP_400_BAD_REQUEST)
            user.subjects.add(follow_subject)
            user.save()
            return Response({'msg': 'User followed subject'}, status=status.HTTP_201_CREATED)
        elif query and query['action'] == 'get_schedule':
            schedule_list = user.lesson_date.filter(confirmation=query.get('approved', False))
            serializer = ScheduleSerializer(schedule_list, many=True)
            return Response({'items': serializer.data})
        serializer = UserSerializer(user)
        return Response({'items': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data['data']
        data['subjects'] = data.get('subjects', [])
        data['users'] = data.get('users', [])
        data['schedule'] = data.get('schedule', [])
        serializer = UserSerializer(data=request.data['data'])
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = user_model.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, data=request.data['data'])
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = user_model.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['post'])
    def telegram_sign_in(self, request, **kwargs):
        data = request.data['data']
        queryset_user = user_model.objects.all()
        user = get_object_or_404(queryset_user, telegram_id=data['telegram_id'])
        user_serializer = UserSerializer(user)
        return Response({'msg': 'You are in Authorized', 'items': user_serializer.data})

    @action(detail=True, methods=['post'])
    def telegram_sign_up(self, request, **kwargs):
        serializer = UserSerializer(data=request.data['data'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class SchedulesViewSet(viewsets.ViewSet):

    def list(self, request):
        query = request.query_params
        if query:
            queryset = scheduling_model.objects.filter(confirmation=query['confirmation'])
        else:
            queryset = scheduling_model.objects.all()
        serializer = ScheduleSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = request.query_params
        queryset = scheduling_model.objects.all()
        schedule = get_object_or_404(queryset, pk=pk)
        if query:
            if query.get('set_conformation') == 'True':
                schedule.confirmation = True
                schedule.save()
                student = schedule.users.filter(is_teacher=False).first()
                method = "sendMessage"
                token = "1317578331:AAEuCDPqvBDHMA68aWVuD5KdBAE92joNAqw"
                url = f"https://api.telegram.org/bot{token}/{method}"
                data = {"chat_id": student.telegram_id,
                        "text": 'teacher approved lesson'}
                requests.post(url, data=data)
                return Response({'msg': 'Lesson approved by teacher'},
                                status=status.HTTP_201_CREATED)
            else:
                schedule.delete()
                return Response({'msg': 'Teacher canceled lesson'}, status=status.HTTP_204_NO_CONTENT)
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data)

    def create(self, request):
        data = request.data['data']
        serializer = ScheduleSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = scheduling_model.objects.all()
        schedule = get_object_or_404(queryset, pk=pk)
        serializer = ScheduleSerializer(schedule, data=request.data['data'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = scheduling_model.objects.all()
        schedule = get_object_or_404(queryset, pk=pk)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def home(request):
    return JsonResponse({'data': {'msg': 'Home page', 'title': 'Home'}},
                        safe=False)


@api_view(['GET'])
def about(request):
    return JsonResponse({'data': {'msg': 'About page', 'title': 'About'}},
                        safe=False)
