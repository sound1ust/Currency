import uuid

from converter.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class UserTask(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID',
    )
    name = models.CharField(
        max_length=128,
        verbose_name='Name',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='user_tasks',
        related_query_name='user_task',
        verbose_name='User',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )
    # START PARAMS
    date_from = models.DateTimeField(
        verbose_name='Date from',
        blank=True,
        null=True,
    )
    date_to = models.DateTimeField(
        verbose_name='Date to',
        blank=True,
        null=True,
    )
    input_tickers = ArrayField(
        base_field=models.CharField(max_length=10),
        default=list,
        verbose_name='Input tickers',
        blank=True,
        null=True,
    )
    output_tickers = ArrayField(
        base_field=models.CharField(max_length=10),
        default=list,
        verbose_name='Output tickers',
        blank=True,
        null=True,
    )
    value_from = models.DecimalField(
        max_digits=24,
        decimal_places=10,
        verbose_name='Value from',
        blank=True,
        null=True,
    )
    value_to = models.DecimalField(
        max_digits=24,
        decimal_places=10,
        verbose_name='Value to',
        blank=True,
        null=True,
    )
    sources = ArrayField(
        base_field=models.CharField(max_length=10),
        default=list,
        verbose_name='Sources',
        blank=True,
        null=True,
    )
    updated_by = ArrayField(
        base_field=models.CharField(max_length=100),
        default=list,
        verbose_name='Updated by',
        blank=True,
        null=True,
    )


class UserTaskResult(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID',
    )
    name = models.CharField(
        max_length=128,
        verbose_name='Name',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='user_tasks_results',
        related_query_name='user_task_result',
        verbose_name='User',
    )
    status = models.CharField(
        max_length=7,
        default='PENDING',
        verbose_name='Status',
        help_text='User task status in the moment',
    )
    start_date = models.DateTimeField(
        verbose_name='Start date',
        help_text='User task working start date',
        blank=True,
        null=True,
        default=None,
    )
    duration = models.DurationField(
        verbose_name='Duration',
        help_text='User task working duration',
        blank=True,
        null=True,
        default=None,
    )
    result_link = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        default=None,
        verbose_name='Result link',
        help_text='User task result link',
    )
    start_parameters = models.CharField(
        max_length=256,
        verbose_name='Start parameters',
    )
