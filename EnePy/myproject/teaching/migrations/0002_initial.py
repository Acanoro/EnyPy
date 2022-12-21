# Generated by Django 4.1.2 on 2022-12-17 06:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teaching', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskusers',
            name='id_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tasks',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, related_name='TaskUsers', to=settings.AUTH_USER_MODEL),
        ),
    ]