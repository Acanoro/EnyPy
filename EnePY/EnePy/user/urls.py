from django.urls import path

from .views import *

urlpatterns = [
    path('personal_area/', personal_area, name='personal_area'),

    path('personal_area/groups/', groups, name='groups'),
    path('teacher_personal_account/groups/group/<int:group_id>/', group, name='group'),

    path('student_personal_account/tasks/', task_statistics, name='student_tasks'),
    path('student_personal_account/control/', test_statistics, name='student_control'),

    path('gsda', get_student_data_ajax),
    path('down_file', down_file),
    path('add_group', add_group),
    path('delete_group', delete_group),
]
