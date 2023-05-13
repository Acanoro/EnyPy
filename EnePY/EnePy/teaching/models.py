from django.urls import reverse
from django.db import models

from user.models import Teachers, Students, CustomUser


# Create your models here.

class ControlWorks(models.Model):
    id_teacher = models.ForeignKey(Teachers, on_delete=models.SET_NULL, null=True, verbose_name='id преподователя')
    name = models.CharField(max_length=100, verbose_name='Название контрольной работы', null=True)
    number_options = models.IntegerField(max_length=30, verbose_name='Количество вариантов')
    number_attempts = models.IntegerField(verbose_name='Количество попыток')
    time_pass = models.DurationField()
    time_start = models.DateTimeField(verbose_name='Начало работы')
    time_end = models.DateTimeField(verbose_name='Конец работы')
    passing_score = models.IntegerField(verbose_name='Количество баллов')

    def get_absolute_url(self):
        return reverse('control', kwargs={'control_id': self.pk})

    def get_absolute_url_1(self):
        return reverse('results', kwargs={'control_id': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контрольные работы'
        verbose_name_plural = 'Контрольные работы'


class Tasks(models.Model):
    id_teacher = models.ForeignKey(Teachers, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name='id преподователя')
    name_task = models.CharField(max_length=50, verbose_name='Название задач')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL', null=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=True)
    data_input = models.JSONField(blank=True, null=True, verbose_name='Входные данные')
    additional_input = models.JSONField(blank=True, null=True, verbose_name='Дополнительные входные данные')
    data_output = models.JSONField(blank=True, null=True, verbose_name='выходные данные')
    status_publ = models.BooleanField(default=False, verbose_name='Статус публикации')
    number_points = models.IntegerField(max_length=2, verbose_name='Количество баллов')

    def get_absolute_url(self):
        return reverse('task', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.name_task

    class Meta:
        verbose_name = 'Задачи'
        verbose_name_plural = 'Задачи'
        ordering = ['order']


class TasksControl(models.Model):
    id_control_work = models.ForeignKey(ControlWorks, on_delete=models.SET_NULL, null=True,
                                        verbose_name='id контрольной работы')
    id_task = models.ForeignKey(Tasks, on_delete=models.SET_NULL, null=True, verbose_name='id задачи')
    id_stud = models.ForeignKey(Students, on_delete=models.SET_NULL, null=True, verbose_name='id студента')
    code = models.TextField(null=True, default=False)
    status_task = models.BooleanField(default=False, verbose_name='Статус задачи')

    class Meta:
        verbose_name = 'Задачи/контрольные'
        verbose_name_plural = 'Задачи/контрольные'


class ControlWorkStatus(models.Model):
    id_control_work = models.ForeignKey(ControlWorks, on_delete=models.SET_NULL, null=True,
                                        verbose_name='id контрольной работы')
    id_stud = models.ForeignKey(Students, on_delete=models.SET_NULL, null=True, verbose_name='id студента')
    time_start = models.DateTimeField(verbose_name='Начало работы')
    time_end = models.DateTimeField(verbose_name='Конец работы')


class TrainingsTasks(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name='id пользователь')
    date_train = models.DateTimeField(verbose_name='Дата выполнения', null=True)
    id_task = models.ForeignKey(Tasks, on_delete=models.SET_NULL, null=True, verbose_name='id задачи')
    code = models.TextField(null=True, blank=False)
    status_task = models.BooleanField(default=False, verbose_name='Статус задачи')
