from django.contrib import admin
from .models import Converter, Source


@admin.register(Converter)
class ConverterAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'original_currency', 'target_currency',
                    'value', 'coefficient', 'source', 'source_date',
                    'updated_at', 'updated_by')
    list_filter = ('created_at', 'original_currency', 'target_currency',
                   'value', 'source', 'source_date', 'updated_at',
                   'updated_by')
    search_fields = ('created_at', 'original_currency', 'target_currency',
                     'value', 'coefficient', 'source', 'source_date',
                     'updated_at', 'updated_by')
    fields = ('created_at', ('original_currency', 'target_currency'),
              ('value', 'coefficient'), ('source', 'source_date'),
              ('updated_at', 'updated_by'))
    readonly_fields = ('created_at',)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'is_active', 'name',
                    'method', 'link', 'tickets')
    list_filter = ('created_at', 'is_active', 'name',
                   'method', 'link', 'tickets')
    search_fields = ('created_at', 'is_active', 'name',
                     'method', 'link', 'tickets')
    fields = ('created_at', 'is_active', 'name',
              'method', 'link', 'tickets')
    readonly_fields = ('created_at',)
