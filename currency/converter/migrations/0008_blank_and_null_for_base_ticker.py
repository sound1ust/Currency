# Generated by Django 2.2.7 on 2023-11-07 09:15
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0007_incr_tickers_values_max'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='base_ticker',
            field=models.CharField(
                blank=True,
                help_text='Base currency that is using as reference in '
                'the source',
                max_length=10,
                null=True,
                verbose_name='Base ticker',
            ),
        ),
    ]