from django.db import models
from django.utils.timezone import now


class Subject(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=350, blank=True, null=True)
    users = models.ManyToManyField('users.CustomUser', blank=True, null=True, related_name='subjects')

    class Meta:
        ordering = ['title']

    def __repr__(self):
        return f'<Subject {self.title}>'


class Scheduling(models.Model):
    confirmation = models.BooleanField(default=False)
    lesson_time = models.DateTimeField(default=now())
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True, related_name='lesson_time')
    users = models.ManyToManyField('users.CustomUser', blank=True, null=True, related_name='lesson_date')

    class Meta:
        ordering = ['lesson_time']

    def __repr__(self):
        return f'<Scheduling {self.lesson_time} -- {self.confirmation}>'
