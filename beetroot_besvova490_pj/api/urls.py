from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='api-home'),
    path('about', views.about, name='api-abouts'),
    path('users', views.users, name='api-users'),
    path('subjects', views.subjects, name='api-subjects'),
    path('schedule', views.schedules, name='api-schedule'),
]