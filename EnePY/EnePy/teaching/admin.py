from django.contrib import admin

# Register your models here.
from .models import *
from django_json_widget.widgets import JSONEditorWidget
from adminsortable2.admin import SortableAdminMixin


class TasksAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'id_teacher', 'name_task', 'status_publ', 'order')
    list_display_links = ('id', 'name_task')
    search_fields = ('id_teacher', 'name_task', 'status_publ')
    list_editable = ('status_publ',)
    list_filter = ('id_teacher', 'name_task', 'status_publ', 'id_teacher')
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    ordering = ['order']
    prepopulated_fields = {
        "slug": ("name_task",)
    }


class TasksControlAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_control_work', 'id_task', 'id_stud', 'status_task')
    list_display_links = ('id',)
    search_fields = ('id_control_work',)
    list_editable = ('status_task',)
    list_filter = ('id_control_work',)


admin.site.register(ControlWorks)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(TasksControl, TasksControlAdmin)
admin.site.register(TrainingsTasks)
admin.site.register(ControlWorkStatus)
