from django.contrib import admin
from . import models


@admin.register(models.Calendar)
class CalendarAdmin(admin.ModelAdmin):
    fields = ('author', 'name', 'members')
    ordering = ('-id',)
    list_display = ('author', 'name', 'date_created')
    list_per_page = 25
    list_filter = ('date_created',)
    show_full_result_count = True


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ('calendar', 'author', 'name', 'description', 'date_start', 'date_end')
    ordering = ('-id',)
    list_display = ('calendar', 'author', 'name', 'date_start', 'date_end')
    list_per_page = 25
    show_full_result_count = True
