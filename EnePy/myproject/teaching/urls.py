from django.urls import path

from .views import *

urlpatterns = [
    path('tasks/', tasks, name='tasks'),
    path('tasks/<int:task_id>/', tasks, name='task'),

    path('task/<int:id_task>/answer/', answer, name='answer'),
    path('tv', tv),

]
