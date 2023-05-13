import xlsxwriter
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from user.forms import *
from user.models import *


# Create your views here.

def personal_area(request):
    user = request.user

    if Teachers.objects.filter(id_user=user).exists():
        teacher = True
    else:
        teacher = False

    if Students.objects.filter(id_user=user).exists():
        students = True
    else:
        students = False

    context = {
        'title': 'EnePy|Личный кабинет',
        'teacher': teacher,
        'students': students,
        'user': True,
    }

    return render(request, 'user/personal_area.html', context=context)


def groups(request):
    group_list = GroupsTeachers.objects.filter(id_user=request.user)
    # tg = GroupTeacher.objects.filter(id_user=request.user.pk)
    form = ChoiceGroupForm()  # , 'groups': tg

    # print(type(group_list[0].id_group))

    # def get_absolute_url(self):
    #     return reverse('teacherGroup', kwargs={'group_id': self.pk})

    context = {'title': 'EnePy|Группы', 'groups': group_list, 'form': form}

    return render(request, 'user/groups.html', context=context)


def group(request, group_id):
    user = request.user.pk
    teacher = Teachers.objects.filter(id_user=user)[0]
    ccwf = ChoiceControlWorkForm()
    group_object = GroupsTeachers.objects.filter(id_group=group_id)

    # request.session['id_group'] = tg[0].id_group.pk
    #

    student_list = Students.objects.filter(id_group=group_id)

    cw = ControlWorks.objects.filter(id_teacher=teacher)

    context = {
        'title': 'EnePy|Группа_№',
        'form': ccwf,
        'name_group': group_object[0].id_group,
        'students': student_list,
        'control_works': cw,
    }

    return render(request, 'user/group.html', context=context)


def task_statistics(request):
    list_solved_problems = []

    id_tasks = []
    tt = TrainingsTasks.objects.filter(id_user=request.user.pk)

    for i in tt:
        if i.id_task.pk not in id_tasks:
            id_tasks.append(i.id_task.pk)
            list_solved_problems.append({
                'id_task': i.id_task.pk,
                'post_slug': i.id_task.slug,
                'task': i.id_task,
                'name_task': i.id_task.name_task,
                'task_code': i.code,
                'solution': i.status_task,
            })
        else:
            for j in range(len(list_solved_problems)):
                if list_solved_problems[j]['id_task'] == i.id_task.pk and not list_solved_problems[j][
                    'solution'] and i.status_task:
                    list_solved_problems[j]['solution'] = True
                    list_solved_problems[j]['task_code'] = i.code

    context = {'title': 'EnePy|Группы', 'task_result': list_solved_problems}

    return render(request, 'user/task_statistics.html', context=context)


def test_statistics(request):
    data_fill = []

    id_stud = Students.objects.filter(id_user=request.user.pk)[0].pk
    co = TasksControl.objects.filter(id_stud=id_stud)

    for i in co:
        data_fill.append({
            'pk': i.id_control_work.pk,
            'name_kr': i.id_control_work.name,
            'task': i.id_task.name_task,
            'solution': i.status_task,
        })

    # id_kr_list = []
    # исправить
    # for i in co:
    #     if i.id_control_work.pk in id_kr_list:
    #         for j in range(len(data_fill)):
    #             if data_fill[j]['pk'] == i.id_control_work.pk and not data_fill[j]['solution'] and i.status_task:
    #                 data_fill[j]['solution'] = True
    #     else:
    #         id_kr_list.append(i.id_control_work.pk)
    #
    #         data_fill.append(
    #             {'pk': i.id_control_work.pk, 'name_kr': i.id_control_work.name, 'task': i.id_task.name_task,
    #              'solution': i.status_task, })

    # print(data_fill)
    context = {'title': 'EnePy|Группы', 'data_fill': data_fill}

    return render(request, 'user/test_statistics.html', context=context)


def get_student_data_ajax(request):
    student_data = []

    id_kr = request.POST['id_kr']

    tc = TasksControl.objects.filter(id_control_work=id_kr)

    for i in tc:
        user = f'{i.id_stud.id_user.last_name} {i.id_stud.id_user.first_name} {i.id_stud.id_user.patronymic}'

        if user in [sd['user'] for sd in student_data]:
            for num, j in enumerate(student_data):
                if j['user'] == user:
                    student_data[num]['tasks'].append({
                        'name_task': i.id_task.name_task,
                        'solution': i.status_task
                    })
        else:
            student_data.append({
                'user': user,
                'name_kr': i.id_control_work.name,
                'number_option': i.id_stud.variant_number,
                'tasks': [{
                    'name_task': i.id_task.name_task,
                    'solution': i.status_task
                }]
            })

    return JsonResponse({'student_data': student_data})


def down_file(request):
    student_data = []
    student_data_new_list = []

    id_control = ControlWorks.objects.filter(pk=request.POST['number_kr'])[0].pk

    tc = TasksControl.objects.filter(id_control_work=id_control)

    for i in tc:
        user = f'{i.id_stud.id_user.last_name} {i.id_stud.id_user.first_name} {i.id_stud.id_user.patronymic}'

        if user in [sd['user'] for sd in student_data]:
            for num, j in enumerate(student_data):
                if j['user'] == user:
                    student_data[num]['tasks'].append({
                        'name_task': i.id_task.name_task,
                        'solution': i.status_task,
                        'number_points': i.id_task.number_points,
                    })
        else:
            student_data.append({
                'user': user,
                'name_kr': i.id_control_work.name,
                'number_option': i.id_stud.variant_number,
                'tasks': [{
                    'name_task': i.id_task.name_task,
                    'solution': i.status_task,
                    'number_points': i.id_task.number_points,
                }]
            })

    number_lines = 6 + len(student_data[0]['tasks'])

    names_first_cells = ['Фамилия', 'Имя', 'Отчество', 'Название кр', 'Номер варианта']

    for i in range(len(student_data[0]['tasks'])):
        names_first_cells.append(str(i + 1) + " задача")

    names_first_cells.append('Общий балл')

    for k, i in enumerate(student_data):
        total_score = 0

        student_data_new_list.append(
            [i['user'].split()[0], i['user'].split()[1], i['user'].split()[2], str(i['name_kr']),
             int(i['number_option'])])

        for j in student_data[k]['tasks']:
            if j['solution']:
                student_data_new_list[k].append(j['number_points'])
                total_score += j['number_points']
            else:
                student_data_new_list[k].append(0)

        student_data_new_list[k].append(total_score)

    work_book = xlsxwriter.Workbook('group_date.xlsx')

    work_sheet = work_book.add_worksheet()

    for i in range(len(student_data) + 1):
        for j in range(number_lines):
            if i == 0:
                work_sheet.write(i, j, names_first_cells[j])
            else:
                work_sheet.write(i, j, student_data_new_list[i - 1][j])

    work_book.close()

    with open('/home/Enepy/EnePy/group_date.xlsx', 'rb') as model_excel:
        result = model_excel.read()

    response = HttpResponse(result)

    response['Content-Disposition'] = 'attachment; filename=test.xlsx'

    return response


def add_group(request):
    user = request.user
    id_group = request.POST['number_group']

    if GroupsTeachers.objects.filter(id_user=user, id_group=id_group).exists():
        return redirect('groups')
    else:
        gt_entry = GroupsTeachers()
        gt_entry.id_user = user
        gt_entry.id_group = Groups.objects.filter(pk=id_group)[0]
        gt_entry.save()
        return redirect('groups')


def delete_group(request):
    id_groups = Groups.objects.filter(pk=request.POST['checkbox'])

    for id_group in id_groups:
        gt = GroupsTeachers.objects.get(id_group=id_group.pk)
        gt.delete()

    return redirect('groups')
