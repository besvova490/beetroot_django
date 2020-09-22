from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import UserSerializer, SubjectSerializer, ScheduleSerializer
from .serializers import user_model, subject_model, scheduling_model


@api_view(['GET'])
def home(request):
    return JsonResponse({'data': {'msg': 'Home page', 'title': 'Home'}},
                        safe=False)


@api_view(['GET'])
def about(request):
    return JsonResponse({'data': {'msg': 'About page', 'title': 'About'}},
                        safe=False)


@api_view(['GET'])
def users(request):
    user_list = user_model.objects.all()
    serializer = UserSerializer(user_list, many=True)
    return JsonResponse({'data': {'msg': 'Users list', 'title': 'About',
                                  'items': serializer.data}},
                        safe=False, status=200)


@api_view(['GET'])
def subjects(request):
    subject_list = subject_model.objects.all()
    serializer = SubjectSerializer(subject_list, many=True)
    return JsonResponse({'data': {'msg': 'Subjects list', 'title': 'About',
                                  'items': serializer.data}},
                        safe=False, status=200)


@api_view(['GET'])
def schedules(request):
    schedule_list = scheduling_model.objects.all()
    serializer = ScheduleSerializer(schedule_list, many=True)
    return JsonResponse({'data': {'msg': 'Schedule list', 'title': 'About',
                                  'items': serializer.data}},
                        safe=False, status=200)
