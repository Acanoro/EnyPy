from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class TeachersAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_user')
    list_display_links = ('id', 'id_user')
    search_fields = ('id_user',)


class StudentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_user', 'id_group', 'variant_number')
    list_display_links = ('id', 'id_user')
    search_fields = ('id_user', 'id_group')
    list_filter = ('id_user', 'id_group')


class GroupsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class GroupsTeachersAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_user', 'id_group')
    search_fields = ('id_user', 'id_group')
    list_filter = ('id_user', 'id_group')


admin.site.register(Teachers, TeachersAdmin)
admin.site.register(Students, StudentsAdmin)
admin.site.register(Groups, GroupsAdmin)
admin.site.register(GroupsTeachers, GroupsTeachersAdmin)


# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Edit user# Edit user
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'patronymic',
                )
            }
        )
    )

    # # Edit user
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'patronymic',
                )
            }
        )
    )

# admin.site.register(NewUser, UserAdmin)
