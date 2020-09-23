from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('subjects', views.SubjectViewSet, basename='subjects')
router.register('schedule', views.SchedulesViewSet, basename='schedule')

urlpatterns = [
    path('in/', include(router.urls)),
    path('in/users/<int:pk>/follow-user/<int:target_id>/', views.UserViewSet.as_view({'get': 'follow_user'})),
    path('in/users/<int:pk>/follow-subject/<int:subject_id>/', views.UserViewSet.as_view({'get': 'follow_subject'})),
    path('', views.home, name='api-home'),
    path('about', views.about, name='api-abouts'),
    path('schedule', views.schedules, name='api-schedule'),
]