from celery import shared_task
from converter.models import Converter, User
from datetime import datetime

import requests
import xmltodict


@shared_task
def get_currency():
    request = requests.request('GET', 'https://www.cbr.ru/scripts/XML_daily.asp')
    data = xmltodict.parse(request.content)['ValCurs']['Valute'][13]

    original_currency = data['CharCode']
    target_currency = 'RUB'
    value = float(data['Value'].replace(',', '.'))
    coefficient = int(data['Nominal'])
    source = 'CBR'
    updated_at = datetime.now()
    updated_by = User.objects.first()

    object = Converter.objects.create(original_currency=original_currency,
                                      target_currency=target_currency,
                                      value=value,
                                      coefficient=coefficient,
                                      source=source,
                                      updated_at=updated_at,
                                      updated_by=updated_by)
    object.save()


@shared_task
def testing():
    return 'TESTING'
