from django.contrib import admin
from converter.models import Converter, Source
from converter.forms import DatesForm, SourceAdminForm


@admin.register(Converter)
class ConverterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'input_ticker',
        'output_ticker',
        'value',
        'coefficient',
        'source_id',
        'source_date',
        'updated_by'
    )

    list_filter = (
        'created_at',
        'input_ticker',
        'output_ticker',
        'value',
        'source_id',
        'source_date',
        'updated_by'
    )

    fields = (
        'created_at',
        ('input_ticker', 'output_ticker'),
        ('value', 'coefficient'),
        ('source_id', 'source_date'),
        ('updated_by',)
    )

    readonly_fields = ('created_at',)

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['form'] = DatesForm(request.GET)
        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        response = super().get_queryset(request)

        if 'start_date' in request.GET and 'end_date' in request.GET:
            start_date = request.GET['start_date']
            end_date = request.GET['end_date']
            if start_date and end_date:
                response = response.filter(created_at__range=[
                    start_date, end_date
                ])

        return response


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    form = SourceAdminForm

    list_display = (
        'id',
        'created_at',
        'name',
        'autoload_method',
        'base_ticker',
        'tickers',
        'last_run_result',
        'last_run_time',
        'is_active'
    )

    list_filter = (
        'created_at',
        'name',
        'autoload_method',
        'base_ticker',
        'is_active'
    )

    fields = (
        'created_at',
        'name',
        'autoload_method',
        'base_ticker',
        'tickers',
        'last_run_result',
        'last_run_time',
        'is_active',
    )

    readonly_fields = ('created_at',)
