from django.shortcuts import render
from teaching.models import TaskUsers, Tasks


# Create your views here.

def user_account(request):
    if request.user.is_authenticated:
        return render(request, 'user/lk_stud_index.html', {'title': 'EnePy|Личный кабинет'})


def tasks(request):
    list_solved_problems = []
    sp = TaskUsers.objects.filter(id_user=request.user.pk)
    if sp:
        for i in sp:
            task = Tasks.objects.filter(name=i.id_tasks.name)
            list_solved_problems.append(
                {'name_task': i.id_tasks.name, 'solution': i.solution, 'code': i.code, 'task': task[0]})

    return render(request, 'user/lk_studenta_var.html',
                  {'title': 'EnePy|Личный кабинет', 'task_result': list_solved_problems})
