from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth.models import User

from converter.consts import AUTOLOAD_METHOD_CHOICES
from django.contrib.postgres.fields import JSONField


class Source(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )
    name = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Name',
    )
    autoload_method = models.CharField(
        max_length=100,
        verbose_name='Autoload method',
        choices=AUTOLOAD_METHOD_CHOICES,
        default=AUTOLOAD_METHOD_CHOICES[0][0],
        help_text='The name of the method used to extract data from the source',
    )
    base_ticker = models.CharField(
        max_length=3,
        verbose_name='Base ticker',
        help_text='Base currency that is using as reference in the source',
    )
    tickers = ArrayField(
        base_field=models.CharField(max_length=3),
        default=list,
        verbose_name='Tickers',
        help_text='Tickers that are converting from the base one',
    )
    last_run_result = JSONField(
        default=dict,
        verbose_name='Last run result',
        help_text='Shows was there any errors in the last run',
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is active',
    )

    class Meta:
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'

    def __str__(self):
        return self.name


class Converter(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )
    input_ticker = models.CharField(
        max_length=3,
        verbose_name='Input ticker',
        help_text='The ticker that converting into the base one',
    )
    output_ticker = models.CharField(
        max_length=3,
        verbose_name='Output ticker',
        help_text='Base currency that is using as reference in the source',
    )
    value = models.FloatField(
        verbose_name='Value',
    )
    coefficient = models.IntegerField(
        verbose_name='Coefficient',
    )
    source_id = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name='converters',
        related_query_name='converter',
        verbose_name='Source',
        help_text='Source where the currency data was taken',
    )
    source_date = models.DateTimeField(
        verbose_name='Source date',
        help_text='The source data date',
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='converters',
        related_query_name='converter',
        verbose_name='Updated by',
    )

    class Meta:
        verbose_name = 'Converter'
        verbose_name_plural = 'Converters'

    def __str__(self):
        return f"{self.input_ticker} / {self.output_ticker}"
