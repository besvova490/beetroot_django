from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, renderers
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UserSerializer, SubjectSerializer, ScheduleSerializer
from .serializers import user_model, subject_model, scheduling_model


class SubjectViewSet(viewsets.ViewSet):

    def list(self, request):
        subject_list = subject_model.objects.all()
        serializer = SubjectSerializer(subject_list, many=True)
        return Response({'data': {
            'msg': 'Subjects list', 'title': 'About',
            'items': serializer.data}}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = subject_model.objects.all()
        subject = get_object_or_404(queryset, pk=pk)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    def create(self, request):
        data = request.data['data']
        data['users'] = data.get('users', [])
        data['schedule'] = data.get('schedule', [])
        serializer = SubjectSerializer(data=request.data['data'])
        if serializer.is_valid():
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
        queryset = user_model.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = user_model.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        data = request.data['data']
        data['subjects'] = data.get('subjects', [])
        data['users'] = data.get('users', [])
        data['schedule'] = data.get('schedule', [])
        serializer = UserSerializer(data=request.data['data'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        data = request.data['data']
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

    @action(detail=True)
    def follow_user(self, request, pk=None, **kwargs):
        print(kwargs)
        return Response({'test': f'user {pk} - {kwargs["target_id"]}'})

    @action(detail=True)
    def follow_subject(self, request, pk=None, **kwargs):
        print(kwargs)
        return Response({'test': f'subject {pk} - {kwargs["subject_id"]}'})


class SchedulesViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = scheduling_model.objects.all()
        serializer = ScheduleSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = scheduling_model.objects.all()
        schedule = get_object_or_404(queryset, pk=pk)
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data)

    def create(self, request):
        try:
            data = request.data['data']
            if len(data['users']) < 2 or not data['subject']:
                return Response({
                    'msg': 'Sms wrong. Please check data'
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer = ScheduleSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.error_messages,
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


@api_view(['GET'])
def schedules(request):
    schedule_list = scheduling_model.objects.all()
    serializer = ScheduleSerializer(schedule_list, many=True)
    return JsonResponse({'data': {'msg': 'Schedule list', 'title': 'About',
                                  'items': serializer.data}},
                        safe=False, status=200)
