from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    is_teacher = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    telegram_id = models.IntegerField(blank=True, null=True)
    users = models.ManyToManyField('self', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        user = self
        user.password = make_password(user.password.strip())
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
