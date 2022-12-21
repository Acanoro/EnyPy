from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from teaching.task_verification import TaskVerification
from teaching.models import *


# Create your views here.


def answer(request, id_task):
    return render(request, 'teaching/zadacha_otvet.html', context={'id_task': id_task})


def tasks(request, task_id=1):
    task_list = []

    tasks = Tasks.objects.all()
    for task in tasks:
        task_list.append({"task": task})

    for i in range(len(task_list)):
        task_answer = TaskUsers.objects.filter(id_user=request.user.pk, id_tasks=task_list[i]["task"].pk)
        if task_answer:
            if task_answer[0].solution:
                task_list[i]["answer"] = 1
            else:
                task_list[i]["answer"] = 0
        else:
            task_list[i]["answer"] = 3

    date_task = get_object_or_404(Tasks, pk=task_id)

    context = {
        'title': f'EnePy|задача {task_id}',
        'tasks': task_list,
        'date_task': date_task,
        'task_selected': task_id
    }

    return render(request, 'teaching/zadacha.html', context=context)


def tv(request):
    code = request.POST['code']
    id_task = request.POST['id_task']
    id_user = request.user

    date_task = get_object_or_404(Tasks, pk=int(id_task))

    login_data_str = date_task.login_data_str

    answer_str = date_task.answer_str

    task_verification = TaskVerification(value_list=login_data_str, answer_list=answer_str, text=code)
    task_verification_answer = task_verification.run()

    # print()
    if request.user.is_authenticated:
        tu = TaskUsers.objects.filter(id_user=id_user, id_tasks=id_task)

        if task_verification_answer[0]:  # если задача решина верно
            if tu:  # если список tu не пустой
                if not tu[0].solution:  # если solution false
                    tu_entry = TaskUsers.objects.get(id_user=id_user, id_tasks=id_task)
                    tu_entry.id_user = id_user
                    tu_entry.id_tasks = date_task
                    tu_entry.code = code
                    tu_entry.solution = True

                    tu_entry.save()
            else:
                tu_entry = TaskUsers()
                tu_entry.id_user = id_user
                tu_entry.id_tasks = date_task
                tu_entry.code = code
                tu_entry.solution = True
                tu_entry.save()
        else:
            if not tu:  # если список tu пустой
                tu_entry = TaskUsers()
                tu_entry.user = id_user
                tu_entry.id_tasks = date_task
                tu_entry.code = code
                tu_entry.solution = False
                tu_entry.save()

    return JsonResponse({'answer': task_verification_answer[0], 'error': str(task_verification_answer[1])})
