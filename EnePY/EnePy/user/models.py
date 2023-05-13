from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


# Create your models here.

class CustomUser(AbstractUser):
    patronymic = models.CharField('Отчество', max_length=64, default='')

    def __str__(self):
        return self.username


class Teachers(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name='id пользователя')

    def __str__(self):
        return self.id_user.username

    class Meta:
        verbose_name = 'Преподователи'
        verbose_name_plural = 'Преподователи'


class Groups(models.Model):
    name = models.CharField(max_length=10, db_index=True, verbose_name='Название группы')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group', kwargs={'group_id': self.pk})

    class Meta:
        verbose_name = 'Группы'
        verbose_name_plural = 'Группы'


class GroupsTeachers(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name='id пользователя')
    id_group = models.ForeignKey(Groups, on_delete=models.SET_NULL, null=True, verbose_name='id группы')

    class Meta:
        verbose_name = 'Преподователь/группы'
        verbose_name_plural = 'Преподователь/группы'


class Students(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name='id пользователя')
    id_group = models.ForeignKey(Groups, on_delete=models.SET_NULL, null=True, verbose_name='id группы')
    variant_number = models.IntegerField(max_length=30, verbose_name='Номер варианта', default=False)

    def __str__(self):
        return self.id_user.username

    class Meta:
        verbose_name = 'Студенты'
        verbose_name_plural = 'Студенты'
