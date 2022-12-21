from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class CustomUser(AbstractUser):
    patronymic = models.CharField('Отчество', max_length=150, default='')

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
