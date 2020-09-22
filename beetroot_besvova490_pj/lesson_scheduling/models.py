from django.db import models


class Subject(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=350)
    users = models.ManyToManyField('users.CustomUser', blank=True, null=True, related_name='subjects')

    class Meta:
        ordering = ['title']

    def __repr__(self):
        return f'<Subject {self.title}>'


class Scheduling(models.Model):
    confirmation = models.BooleanField(default=False)
    lesson_time = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True, related_name='schedule')
    users = models.ManyToManyField('users.CustomUser', blank=True, null=True, related_name='schedule')

    class Meta:
        ordering = ['lesson_time']

    def __repr__(self):
        return f'<Scheduling {self.lesson_time} -- {self.confirmation}>'
