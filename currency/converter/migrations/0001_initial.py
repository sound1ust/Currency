# Generated by Django 2.2.7 on 2023-09-28 14:28

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=10, unique=True)),
                ('method', models.CharField(max_length=256)),
                ('link', models.CharField(max_length=256)),
                ('tickets', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=3), default=list, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Converter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('original_currency', models.CharField(max_length=3)),
                ('target_currency', models.CharField(max_length=3)),
                ('value', models.FloatField()),
                ('coefficient', models.PositiveIntegerField()),
                ('source', models.CharField(max_length=256)),
                ('source_date', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
