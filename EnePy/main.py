# import xlsxwriter
#
# student_data = [{'user': 'Тумашевич Никита Русланович', 'number_kr': '1', 'number_option': 1,
#                  'tasks': [{'name_task': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqq', 'solution': True},
#                            {'name_task': 'wwwwwwwwwwwwwwwwwwww', 'solution': False}]},
#                 {'user': 'sdsfgh asd Николаевна', 'number_kr': '1', 'number_option': 2,
#                  'tasks': [{'name_task': 'eeeeeeeeeeeeeeeeeeeeeee', 'solution': True},
#                            {'name_task': 'wwwwwwwwwwwwwwwwwwww', 'solution': False}]}]
#
# student_data_new_list = []
#
# number_lines = 6 + len(student_data[0]['tasks'])
#
# names_first_cells = ['Фамилия', 'Имя', 'Отчество', 'Номер кр', 'Номер варианта']
#
# for i in range(len(student_data[0]['tasks'])):
#     names_first_cells.append(str(i + 1) + " задача")
#
# names_first_cells.append('Общий балл')
#
# for k, i in enumerate(student_data):
#     total_score = 0
#
#     student_data_new_list.append(
#         [i['user'].split()[0], i['user'].split()[1], i['user'].split()[2], int(i['number_kr']),
#          int(i['number_option'])])
#
#     for j in student_data[k]['tasks']:
#         if j['solution']:
#             student_data_new_list[k].append(1)
#             total_score += 1
#         else:
#             student_data_new_list[k].append(0)
#
#     student_data_new_list[k].append(total_score)
#
# work_book = xlsxwriter.Workbook('group_date.xlsx')
#
# work_sheet = work_book.add_worksheet()
#
# for i in range(len(student_data) + 1):
#     for j in range(number_lines):
#         if i == 0:
#             work_sheet.write(i, j, names_first_cells[j])
#         else:
#             print(i, j)
#             work_sheet.write(i, j, student_data_new_list[i - 1][j])
#
# work_book.close()
#
# # [['Тумашевич', 'Никита', 'Русланович', '1', 1, 1, 0], ['sdsfgh', 'asd', 'Николаевна', '1', 2, 1]]


