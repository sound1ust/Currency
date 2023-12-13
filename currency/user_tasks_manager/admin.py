from django.contrib import admin
from django.utils.html import format_html
from user_tasks_manager.models import UserTask
from user_tasks_manager.models import UserTaskResult
from user_tasks_manager.tasks import export_task
from user_tasks_manager.utils import normalize_decimal


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
        'normalized_value_from',
        'normalized_value_to',
        'sources_list',
        'updated_by_list',
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

    def sources_list(self, obj):
        return ',\n'.join([str(s) for s in obj.sources.all()])

    sources_list.short_description = 'Sources'

    def updated_by_list(self, obj):
        return ',\n'.join([str(s) for s in obj.updated_by.all()])

    updated_by_list.short_description = 'Updated by'

    def normalized_value_from(self, obj):
        if obj.value_from:
            return normalize_decimal(obj.value_from)

    normalized_value_from.short_description = 'Value from'

    def normalized_value_to(self, obj):
        if obj.value_to:
            return normalize_decimal(obj.value_to)

    normalized_value_to.short_description = 'Value to'


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

    def display_result_link(self, obj):
        if not obj.result_link:
            return None
        return format_html(
            format_string="<a href='{url}'>Download</a>",
            url=obj.result_link,
        )

    display_result_link.short_description = 'Result link'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(UserTaskResult, UserTaskResultAdmin)
