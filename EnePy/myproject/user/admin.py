from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


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
