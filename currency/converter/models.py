from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth.models import User

from converter.consts import AUTOLOAD_METHOD_CHOICES
from django.contrib.postgres.fields import JSONField

class Source(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=10, unique=True)
    method = models.CharField(max_length=256)
    tickets = ArrayField(base_field=models.CharField(max_length=3),
                         default=list)
    last_run_result = JSONField(default=dict)
    autoload_method = models.CharField(
        max_length=100,
        verbose_name='Autoload method',
        choices=AUTOLOAD_METHOD_CHOICES,
        default=AUTOLOAD_METHOD_CHOICES[0][0],
    )
    base_currency = ...


class Converter(models.Model):
    source_type  = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name='converter',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    original_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    value = models.FloatField()
    coefficient = models.PositiveIntegerField()
    source = models.CharField(max_length=256)
    source_date = models.DateTimeField()
    updated_at = models.DateTimeField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)


