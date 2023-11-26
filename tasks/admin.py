from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('get_role_display',)

    def get_role_display(self, obj):
        return obj.get_role_display()
    get_role_display.short_description = _('Role')
    get_role_display.admin_order_field = 'role'

admin.site.register(CustomUser, CustomUserAdmin)
