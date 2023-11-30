from django.contrib import admin
from user_tasks_manager.models import UserTask
from user_tasks_manager.tasks import export_task


def run_tasks(modeladmin, request, queryset):
    for task in queryset:
        export_task.delay(task.id)


run_tasks.short_description = 'Run selected tasks'


class UserTaskAdmin(admin.ModelAdmin):
    actions = [run_tasks]
    list_display = (
        'name',
        'user',
        'start_date',
        'duration',
        'status',
        'result_link',
        'start_parameters',
    )


admin.site.register(UserTask, UserTaskAdmin)
