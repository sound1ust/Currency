from celery import shared_task
from converter.models import Converter, User
from datetime import datetime, timedelta

import requests
import xmltodict


@shared_task
def get_currency():
    request = requests.request('GET', 'https://www.cbr.ru/scripts/XML_daily.asp')
    data = xmltodict.parse(request.content)['ValCurs']['Valute'][13]
    source_date = xmltodict.parse(request.content)['ValCurs']['@Date']

    original_currency = data['CharCode']
    target_currency = 'RUB'
    value = float(data['Value'].replace(',', '.'))
    coefficient = int(data['Nominal'])
    source = 'CBR'
    source_date = datetime.strptime(source_date, '%d.%m.%Y') + timedelta(hours=1)
    updated_at = datetime.now()
    updated_by = User.objects.first()

    last_currency = Converter.objects.filter(original_currency=original_currency,
                                             target_currency=target_currency,
                                             source=source,
                                             updated_by=updated_by).order_by('created_at').last()

    if last_currency.value != value:
        object = Converter.objects.create(original_currency=original_currency,
                                          target_currency=target_currency,
                                          value=value,
                                          coefficient=coefficient,
                                          source=source,
                                          source_date=source_date,
                                          updated_at=updated_at,
                                          updated_by=updated_by)

        object.save()
    else:
        return 'The currency did not change'


@shared_task
def testing():
    return 'TESTING'
