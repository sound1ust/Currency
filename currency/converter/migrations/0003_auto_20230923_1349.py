# Generated by Django 2.2.7 on 2023-09-23 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0002_auto_20230923_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='converter',
            name='value',
            field=models.FloatField(),
        ),
    ]
