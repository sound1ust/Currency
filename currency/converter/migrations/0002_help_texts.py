# Generated by Django 2.2.7 on 2023-09-30 17:51

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='converter',
            old_name='source',
            new_name='source_id',
        ),
        migrations.AlterField(
            model_name='converter',
            name='input_ticker',
            field=models.CharField(help_text='The ticker that converting into the base one', max_length=3, verbose_name='Input ticker'),
        ),
        migrations.AlterField(
            model_name='converter',
            name='output_ticker',
            field=models.CharField(help_text='Base currency that is using as reference in the source', max_length=3, verbose_name='Output ticker'),
        ),
        migrations.AlterField(
            model_name='source',
            name='base_ticker',
            field=models.CharField(help_text='Base currency that is using as reference in the source', max_length=3, verbose_name='Base ticker'),
        ),
        migrations.AlterField(
            model_name='source',
            name='tickers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=3), default=list, help_text='Tickers that are converting from the base one', size=None, verbose_name='Tickers'),
        ),
    ]
