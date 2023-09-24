from django.contrib import admin
from .models import Converter


@admin.register(Converter)
class ConverterAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'original_currency', 'target_currency', 'value', 'coefficient',
                    'source', 'source_date', 'updated_at', 'updated_by')
    list_filter = ('created_at', 'original_currency', 'target_currency', 'value',
                   'source', 'source_date', 'updated_at', 'updated_by')
    search_fields = ('created_at', 'original_currency', 'target_currency', 'value', 'coefficient',
                     'source', 'source_date', 'updated_at', 'updated_by')
    fields = ('created_at', ('original_currency', 'target_currency'), ('value', 'coefficient'),
              ('source', 'source_date'), ('updated_at', 'updated_by'))
    readonly_fields = ('created_at', 'source_date')
