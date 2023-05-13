from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render, get_object_or_404

from teaching.task_verification import TaskVerification
from teaching.models import *


# Create your views here.

def tasks(request, post_slug=None):
    id_user = request.user.pk
    new_task_list = []
    task_list = Tasks.objects.filter(status_publ=True).order_by('order')

    if post_slug:
        current_task = Tasks.objects.filter(status_publ=True, slug=post_slug)
    else:
        current_task = task_list

    current_task_index = list(task_list).index(current_task[0])

    previous_task = task_list[current_task_index - 1] if current_task_index > 0 else None
    next_task = task_list[current_task_index + 1] if current_task_index < len(task_list) - 1 else None

    start_index = max(0, current_task_index - 2)
    end_index = min(len(task_list), current_task_index + 3)

    for i in task_list[start_index:end_index]:
        trainings_tasks = TrainingsTasks.objects.filter(id_user=id_user, id_task=i.pk)
        if trainings_tasks:
            for j in trainings_tasks:
                if j.status_task:
                    solution = j.status_task
                    break
            else:
                solution = False

            new_task_list.append({'task': i, 'solution': solution})
        else:
            new_task_list.append({'task': i, 'solution': None})

    context = {
        'title': f'задачи',
        'kr': False,
        'task': True,
        'task_list': new_task_list,
        'current_task': current_task[0],
        'previous_task': previous_task,
        'next_task': next_task,
    }
    return render(request, 'teaching/zadacha.html', context=context)


def answer(request, post_slug):
    return render(request, 'teaching/zadacha_otvet.html', context={'post_slug': post_slug})


# решить проблему
def tv(request):
    code = request.POST['code']
    post_slug = request.POST['post_slug']
    task_status = request.POST['task']
    kr_status = request.POST['kr']
    id_kr = request.POST['id_kr']

    date_task = get_object_or_404(Tasks, slug=post_slug)
    login_data_str = date_task.data_input
    answer_str = date_task.data_output
    optional_list_values = date_task.additional_input

    task_verification = TaskVerification(value_list=login_data_str, answer_list=answer_str, text=code,
                                         optional_list_values=optional_list_values)
    task_verification_answer = task_verification.run()  # (True, 'Ошибок нет')
    if request.user.is_authenticated:
        if eval(task_status):  # если идет простое решение задач
            tt_entry = TrainingsTasks()
            tt_entry.id_user = request.user
            tt_entry.date_train = timezone.now()
            tt_entry.id_task = date_task
            tt_entry.code = code
            tt_entry.status_task = task_verification_answer[0]
            tt_entry.save()
        elif eval(kr_status):  # если идет кр
            if task_verification_answer[0]:
                id_stud = Students.objects.filter(id_user=request.user)[0]

                kr_obj = ControlWorks.objects.filter(pk=id_kr)[0]

                tc_entry = TasksControl.objects.get(id_control_work=kr_obj.pk, id_stud=id_stud, id_task=date_task.pk)
                # tc_entry.id_control_work = kr_obj
                # tc_entry.id_task = date_task
                # tc_entry.id_stud = id_stud
                tc_entry.code = code
                tc_entry.status_task = task_verification_answer[0]
                tc_entry.save()

    return JsonResponse({'answer': task_verification_answer[0], 'error': str(task_verification_answer[1])})


def controls(request):
    number_attempts_used = []

    id_stud = Students.objects.filter(id_user=request.user)[0].pk
    control_list = ControlWorks.objects.all()
    # control_work_status_list = ControlWorkStatus.objects.filter(id_stud=id_stud)

    for i in control_list:
        control_work_status_list = ControlWorkStatus.objects.filter(id_control_work=i.pk, id_stud=id_stud)

        if control_work_status_list:
            number_attempts_used.append({
                'name': i.name,
                'number_attempts_used': i.number_attempts - len(control_work_status_list),
            })
        else:
            number_attempts_used.append({
                'name': i.name,
                'number_attempts_used': i.number_attempts,
            })

    context = {
        'title': 'Задачи',
        'controls': control_list,
        'number_attempts_used': number_attempts_used,
    }
    return render(request, 'teaching/kontrlonie_autor.html', context=context)


def control(request, control_id):
    kr_obj = ControlWorks.objects.filter(pk=control_id)[0]

    task_slug = request.GET.get('task_slug', 1)
    current_task = None
    previous_task = None
    next_task = None
    remaining_time = None

    new_task_list = []

    if kr_obj.time_start <= timezone.now() <= kr_obj.time_end:
        # если текущее время входит в заданный интервал времени
        student = Students.objects.filter(id_user=request.user)[0]
        cws = ControlWorkStatus.objects.filter(id_control_work=control_id, id_stud=student)

        if len(cws) != kr_obj.number_attempts:
            # если есть еще попытки
            kr_list = TasksControl.objects.filter(id_control_work=control_id, id_stud=student)

            task_list = [i.id_task for i in kr_list]
            ####################################################################################################################################################################
            for i in task_list:
                if task_slug != 1:
                    if i.slug == task_slug:
                        current_task = [i]
                        break
            else:
                current_task = task_list

            current_task_index = list(task_list).index(current_task[0])

            previous_task = task_list[current_task_index - 1] if current_task_index > 0 else None
            next_task = task_list[current_task_index + 1] if current_task_index < len(task_list) - 1 else None

            start_index = max(0, current_task_index - 2)
            end_index = min(len(task_list), current_task_index + 3)

            for i in task_list[start_index:end_index]:
                tasks_control = TasksControl.objects.filter(id_control_work=control_id, id_task=i.pk, id_stud=student)
                if tasks_control:
                    for j in tasks_control:
                        if j.status_task:
                            solution = j.status_task
                            break
                    else:
                        solution = False

                    new_task_list.append({'task': i, 'solution': solution})
                else:
                    new_task_list.append({'task': i, 'solution': None})

            ####################################################################################################################################################################
            if 'start_time' in request.session:
                start_time = request.session['start_time']
            else:
                start_time = timezone.now().isoformat()
                request.session['start_time_r'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                request.session['start_time'] = start_time

                request.session['goes_cr'] = True

            start_time_time = datetime.fromisoformat(start_time)
            decision_time_1 = kr_obj.time_end - kr_obj.time_start
            decision_time_2 = kr_obj.time_pass

            if decision_time_2 <= decision_time_1:
                remaining_time = (start_time_time + decision_time_2) - timezone.now()
            else:
                remaining_time = (start_time_time + decision_time_1) - timezone.now()

        # if remaining_time.total_seconds() < 0:
        #     # Время теста истекло
        #     del request.session['start_time']
        #     return HttpResponse('Время теста истекло')

        else:
            # если нет попыток
            pass

        context = {
            'title': 'Задачи',
            'remaining_time': remaining_time,
            'kr_id': kr_obj,
            'kr': True,
            'task': False,

            'task_list': new_task_list,
            'current_task': current_task[0],
            'previous_task': previous_task,
            'next_task': next_task,
        }

        return render(request, 'teaching/zadacha.html', context=context)

    else:
        # если текущее время не входит в заданный интервал времени
        pass


def results(request, control_id):
    kr_obj = ControlWorks.objects.filter(pk=control_id)[0]
    id_stud = Students.objects.filter(id_user=request.user)[0]
    cws = ControlWorkStatus.objects.filter(id_control_work=control_id).last()

    tc = TasksControl.objects.filter(id_control_work=control_id, id_stud=id_stud.pk)

    id_tasks = []

    task_list = []
    for i in tc:
        if i.id_task.pk in id_tasks:
            for j in range(len(task_list)):
                if task_list[j]['id_task'] == i.id_task.pk and task_list[j]['task_solution'] != True and i.status_task:
                    task_list[j]['task_solution'] = True
        else:
            id_tasks.append(i.id_task.pk)

            task_name = i.id_task.name_task
            task_description = i.id_task.description
            # code = None
            task_solution = i.status_task

            task_list.append({
                'id_task': i.id_task.pk,
                'task_name': task_name,
                'task_description': task_description,
                'task_solution': task_solution,
            })

    points = sum(1 for i in tc if i.status_task)

    if 'start_time' in request.session:
        remaining_time = request.session['start_time_r']
        end_time = str(datetime.strptime(request.GET.get('end_time'), '%Y-%m-%dT%H:%M:%S.%fZ'))[:-7]

        date1 = datetime.strptime(remaining_time, '%Y-%m-%d %H:%M:%S')
        date2 = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        time_passed = date2 - date1

        cws = ControlWorkStatus(id_control_work=kr_obj, id_stud=id_stud, time_start=remaining_time,
                                time_end=end_time)
        cws.save()

        del request.session['start_time']
        del request.session['start_time_r']
        del request.session['goes_cr']

        context = {
            'time_start': remaining_time,
            'time_end': end_time,
            'time_passed': time_passed,
            'points': points,
            'task_list': task_list,
        }
        return render(request, 'teaching/results.html', context=context)
    else:
        time_passed = cws.time_end - cws.time_start
        context = {
            'time_start': cws.time_start,
            'time_end': cws.time_end,
            'time_passed': time_passed,
            'points': points,
            'task_list': task_list,
        }
        return render(request, 'teaching/results.html', context=context)
