from django.contrib import admin
from .models import Converter, Source

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


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'name',
        'autoload_method',
        'base_ticker',
        'tickers',
        'last_run_result',
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
        'is_active',
    )

    readonly_fields = ('created_at',)
