from django.db import models
from django.contrib.auth.models import User


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
