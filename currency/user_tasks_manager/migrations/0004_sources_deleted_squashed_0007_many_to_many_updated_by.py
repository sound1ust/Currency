# Generated by Django 3.2.23 on 2023-12-13 12:00
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    replaces = [
        ('user_tasks_manager', '0004_sources_deleted'),
        ('user_tasks_manager', '0005_many_to_many_sources'),
        ('user_tasks_manager', '0006_updated_by_deleted'),
        ('user_tasks_manager', '0007_many_to_many_updated_by'),
    ]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            'user_tasks_manager',
            '0003_user_task_and_user_task_result_created_squashed_'
            '0006_dates_changes',
        ),
        ('converter', '0008_blank_and_null_for_base_ticker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertask',
            name='sources',
        ),
        migrations.AlterField(
            model_name='usertask',
            name='date_from',
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name='Date from',
            ),
        ),
        migrations.AlterField(
            model_name='usertask',
            name='date_to',
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name='Date to',
            ),
        ),
        migrations.AddField(
            model_name='usertask',
            name='sources',
            field=models.ManyToManyField(
                blank=True,
                help_text='Source where the currency data was taken',
                related_name='user_tasks',
                related_query_name='user_task',
                to='converter.Source',
                verbose_name='Sources',
            ),
        ),
        migrations.RemoveField(
            model_name='usertask',
            name='updated_by',
        ),
        migrations.AddField(
            model_name='usertask',
            name='updated_by',
            field=models.ManyToManyField(
                blank=True,
                related_name='updates_made',
                related_query_name='update_made',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Updated by',
            ),
        ),
    ]