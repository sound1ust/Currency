import uuid

from converter.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from user_tasks_manager.consts import USER_TASK_STATUS_CHOICES


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
    status = models.CharField(
        max_length=7,
        choices=USER_TASK_STATUS_CHOICES,
        default='Pending',
        verbose_name='Status',
        help_text='User task status in the moment',
    )
    result_link = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        default=None,
        verbose_name='Result link',
        help_text='User task result link',
    )
    start_parameters = JSONField(
        verbose_name='Start parameters',
        help_text='Parameters which will configure the result',
    )

    def update_task_status(self, status, result=None):
        self.status = status
        if result:
            self.result_link = result

        self.save()
