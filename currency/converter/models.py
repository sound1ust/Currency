from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth.models import User


class Source(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=10, unique=True)
    method = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    tickets = ArrayField(base_field=models.CharField(max_length=3),
                         default=list)
    # last_run_result = models.CharField(max_length=256)


class Converter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    original_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    value = models.FloatField()
    coefficient = models.PositiveIntegerField()
    source = models.CharField(max_length=256)
    source_date = models.DateTimeField()
    updated_at = models.DateTimeField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)