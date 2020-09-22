from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='api-home'),
    path('about', views.about, name='api-abouts'),
]