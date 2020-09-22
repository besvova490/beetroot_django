import __future__
from rest_framework import serializers
from django.apps import apps

user_model = apps.get_model('users', 'CustomUser')
subject_model = apps.get_model('lesson_scheduling', 'Subject')
scheduling_model = apps.get_model('lesson_scheduling', 'Scheduling')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ['id', 'email', 'first_name', 'last_name', 'is_teacher',
                  'phone_number', 'telegram_id', 'schedule', 'subjects', 'users']


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = subject_model
        fields = ['id', 'title', 'description', 'schedule', 'users']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = scheduling_model
        fields = ['id', 'confirmation', 'lesson_time', 'subject', 'users']
