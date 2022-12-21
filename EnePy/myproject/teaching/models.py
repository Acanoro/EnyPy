from django_jsonform.models.fields import ArrayField
from django.db import models
from django.urls import reverse

from user.models import CustomUser


# Create your models here.


class Tasks(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    login_data_str = ArrayField(ArrayField(models.TextField()), blank=True, null=True, size=10)
    answer_str = ArrayField(ArrayField(models.TextField()), blank=True, null=True, size=10)
    users = models.ManyToManyField(CustomUser, "TaskUsers", blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('task', kwargs={'task_id': self.pk})

    class Meta:
        verbose_name = 'Задачи'
        verbose_name_plural = 'Задачи'


class TaskUsers(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    id_tasks = models.ForeignKey(Tasks, on_delete=models.SET_NULL, null=True)
    code = models.TextField()
    solution = models.BooleanField(blank=True, null=True)

    class Meta:
        verbose_name = 'Задача/Пользователь'
        verbose_name_plural = 'Задача/Пользователь'
