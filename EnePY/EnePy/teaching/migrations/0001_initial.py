# Generated by Django 4.1.7 on 2023-04-16 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ControlWorks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Название контрольной работы')),
                ('number_options', models.IntegerField(max_length=30, verbose_name='Количество вариантов')),
                ('number_attempts', models.IntegerField(verbose_name='Количество попыток')),
                ('time_pass', models.DurationField()),
                ('time_start', models.DateTimeField(verbose_name='Начало работы')),
                ('time_end', models.DateTimeField(verbose_name='Конец работы')),
                ('passing_score', models.IntegerField(verbose_name='Количество баллов')),
            ],
            options={
                'verbose_name': 'Контрольные работы',
                'verbose_name_plural': 'Контрольные работы',
            },
        ),
        migrations.CreateModel(
            name='ControlWorkStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField(verbose_name='Начало работы')),
                ('time_end', models.DateTimeField(verbose_name='Конец работы')),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_task', models.CharField(max_length=50, verbose_name='Название задач')),
                ('description', models.TextField(max_length=1000, verbose_name='Описание')),
                ('slug', models.SlugField(max_length=255, null=True, unique=True, verbose_name='URL')),
                ('order', models.PositiveIntegerField(default=0, null=True)),
                ('data_input', models.JSONField(blank=True, null=True, verbose_name='Входные данные')),
                ('additional_input', models.JSONField(blank=True, null=True, verbose_name='Дополнительные входные данные')),
                ('data_output', models.JSONField(blank=True, null=True, verbose_name='выходные данные')),
                ('status_publ', models.BooleanField(default=False, verbose_name='Статус публикации')),
                ('number_points', models.IntegerField(max_length=2, verbose_name='Количество баллов')),
            ],
            options={
                'verbose_name': 'Задачи',
                'verbose_name_plural': 'Задачи',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TasksControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(default=False, null=True)),
                ('status_task', models.BooleanField(default=False, verbose_name='Статус задачи')),
            ],
            options={
                'verbose_name': 'Задачи/контрольные',
                'verbose_name_plural': 'Задачи/контрольные',
            },
        ),
        migrations.CreateModel(
            name='TrainingsTasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_train', models.DateTimeField(null=True, verbose_name='Дата выполнения')),
                ('code', models.TextField(null=True)),
                ('status_task', models.BooleanField(default=False, verbose_name='Статус задачи')),
                ('id_task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teaching.tasks', verbose_name='id задачи')),
            ],
        ),
    ]
