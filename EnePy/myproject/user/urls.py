from django.urls import path

from .views import *

urlpatterns = [
    path('student_personal_account/', user_account, name='user'),
    path('student_personal_account/tasks/', tasks, name='Tasks'),

]
