from django.contrib import admin
from django.utils.html import format_html
from user_tasks_manager.models import UserTask
from user_tasks_manager.models import UserTaskResult
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
        'created_at',
        'date_from',
        'date_to',
        'input_tickers',
        'output_tickers',
        'value_from',
        'value_to',
        'sources',
        'updated_by',
    )
    fieldsets = (
        (
            'Main',
            {
                'fields': (
                    'name',
                    'user',
                ),
            },
        ),
        (
            'Start Parameters',
            {
                'fields': (
                    'date_from',
                    'date_to',
                    'input_tickers',
                    'output_tickers',
                    'value_from',
                    'value_to',
                    'sources',
                    'updated_by',
                ),
            },
        ),
    )


admin.site.register(UserTask, UserTaskAdmin)


class UserTaskResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'user',
        'status',
        'start_date',
        'duration',
        'display_result_link',
        'start_parameters',
    )
    list_display_links = None

    def display_result_link(self, obj):
        if not obj.result_link:
            return None
        return format_html(
            format_string="<a href='{url}'>Download</a>",
            url=obj.result_link,
        )

    display_result_link.short_description = 'Result link'


admin.site.register(UserTaskResult, UserTaskResultAdmin)
