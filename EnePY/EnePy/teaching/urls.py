from django.urls import path

from .views import *

urlpatterns = [
    path('tasks', tasks, name='tasks'),
    path('task/<slug:post_slug>/', tasks, name='task'),

    path('task/<slug:post_slug>/answer/', answer, name='answer'),
    path('tv', tv),

    path('controls/', controls, name='controls'),
    path('control/<int:control_id>/', control, name='control'),

    path('results/<int:control_id>', results, name='results'),
]
