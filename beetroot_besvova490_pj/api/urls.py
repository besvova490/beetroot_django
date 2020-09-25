from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('subjects', views.SubjectViewSet, basename='subjects')
router.register('schedule', views.SchedulesViewSet, basename='schedule')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/telegram-sign-in', views.UserViewSet.as_view({'post': 'telegram_sign_in'})),
    path('api/telegram-sign-up', views.UserViewSet.as_view({'post': 'telegram_sign_up'})),
    path('', views.home, name='api-home'),
    path('about', views.about, name='api-abouts'),
]