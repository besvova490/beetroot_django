from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def home(request):
    return JsonResponse({'data': {'msg': 'Home page', 'title': 'Home'}},
                        safe=False)


@api_view(['GET'])
def about(request):
    return JsonResponse({'data': {'msg': 'About page', 'title': 'About'}},
                        safe=False)
