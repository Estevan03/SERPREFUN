from django.contrib import admin
from .models import *


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
  readonly_fields = ('created', )

admin.site.register(Task, TaskAdmin)

class CustomUserAdmin(admin.ModelAdmin):
  list_display = ['role']

admin.site.register(CustomUser, CustomUserAdmin)