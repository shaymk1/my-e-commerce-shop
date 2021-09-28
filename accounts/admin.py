from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'username', 'last_login', 'date_created', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_created')
    ordering = ('-date_created',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()  # makes password read only


admin.site.register(Account, AccountAdmin)
