from rest_framework import serializers
from django.apps import apps

user_model = apps.get_model('users', 'CustomUser')
subject_model = apps.get_model('lesson_scheduling', 'Subject')
scheduling_model = apps.get_model('lesson_scheduling', 'Scheduling')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ['id', 'email', 'is_teacher', 'first_name', 'last_name', 'phone_number',
                  'telegram_id', 'lesson_date', 'subjects', 'users']

    def to_representation(self, obj):
        lesson_date = [{'id': schedule.id, 'time': schedule.lesson_time,
                        'status': schedule.confirmation,
                        'subject': schedule.subject.title}
                       for schedule in obj.lesson_date.all()]
        users = [{'id': user.id, 'telegram_id': user.telegram_id,
                  'full_name': f'{user.first_name} {user.last_name}'.strip(),
                  'is_teacher': user.is_teacher, 'email': user.email}
                 for user in obj.users.all()]
        subject = [{'id': subject.id, 'title': subject.title} for subject in
                   obj.subjects.all()]
        return {'id': obj.id,
                'full_name': f'{obj.first_name} {obj.last_name}'.strip(),
                'telegram_id': obj.telegram_id,
                'is_teacher': obj.is_teacher, 'email': obj.email,
                'subjects': subject, 'users': users, 'lesson_date': lesson_date}


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = subject_model
        fields = ['id', 'title', 'description', 'lesson_time', 'users']

    def to_representation(self, obj):
        lesson_date = [{'id': schedule.id, 'time': schedule.lesson_time,
                        'confirmation': schedule.confirmation} for schedule in
                       obj.lesson_time.all()]
        users = [{'id': user.id,
                  'full_name': f'{user.first_name} {user.last_name}'.strip(),
                  'is_teacher': user.is_teacher} for user in obj.users.all()]
        return {'id': obj.id, 'title': obj.title, 'lesson_date': lesson_date,
                'description': obj.description, 'users': users}


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = scheduling_model
        fields = ['id', 'confirmation', 'lesson_time', 'subject', 'users']

    def create(self, validated_data):
        schedule = scheduling_model.objects.create(
            lesson_time=validated_data['lesson_time'],
            subject=validated_data['subject'])
        schedule.users.set(validated_data['users'])
        return schedule

    def to_representation(self, obj):
        users = [{'id': user.id, 'telegram_id': user.telegram_id,
                  'full_name': f'{user.first_name} {user.last_name}'.strip(),
                  'is_teacher': user.is_teacher,
                  'email': user.email} for user in obj.users.all()]
        return {'id': obj.id, 'time': obj.lesson_time,
                'status': obj.confirmation, 'subject': obj.subject.title,
                'users': users}
