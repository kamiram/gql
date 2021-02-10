from django.db import models

from django.contrib.auth.models import AbstractUser


class ApiUser(AbstractUser):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    username = models.CharField('Username', blank=True, max_length=254, )
    email = models.EmailField('EMail', blank=False, max_length=254, unique=True)
    bio = models.TextField('Biography')
    social = models.CharField('Social', blank=True, max_length=50, default='')
