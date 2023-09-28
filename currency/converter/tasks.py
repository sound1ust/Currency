from datetime import datetime, timedelta

import requests
import xmltodict
from celery import shared_task

from converter.models import Converter, User, Source


def get_cbr_data(source_obj, response):
    source_info = xmltodict.parse(response.content).get('ValCurs')

    if source_info:
        date_from_source = source_info.get('@Date')
        all_currency_data = source_info.get('Valute')
    else:
        return 'Invalid data'

    for ticket in source_obj.tickets:

        currency_data = next((val for val in all_currency_data if
                              val.get('CharCode') == ticket))

        if currency_data:
            original_currency = currency_data.get('CharCode')
            target_currency = 'RUB'
            value = currency_data.get('Value')

            if value:
                value = float(value.replace(',', '.'))
            else:
                return 'Invalid value'

            coefficient = int(currency_data.get('Nominal'))
            source_name = source_obj.name

            if date_from_source:
                source_date = datetime.strptime(date_from_source, '%d.%m.%Y') + \
                              timedelta(hours=1)
            else:
                return 'Invalid date'

            updated_at = datetime.now()
            updated_by = User.objects.first()
        else:
            return 'Invalid currency data'

        alike_currencies = Converter.objects.filter(
            original_currency=original_currency,
            target_currency=target_currency,
            source=source_name,
            updated_by=updated_by).order_by('created_at')

        must_save = False

        if alike_currencies:
            last_currency = alike_currencies.last()

            if last_currency.value == value:
                return 'The currency did not change'
            else:
                must_save = True
        else:
            must_save = True

        if must_save:
            Converter.objects.create(
                original_currency=original_currency,
                target_currency=target_currency,
                value=value,
                coefficient=coefficient,
                source=source_name,
                source_date=source_date,
                updated_at=updated_at,
                updated_by=updated_by)


def get_ecb_data(response):
    pass


@shared_task
def get_currency():
    methods = {
        'get_cbr_data': get_cbr_data,
        'get_ecb_data': get_ecb_data,
    }
    sources = Source.objects.filter(is_active=True)
    if not sources:
        return 'No active sources'
    else:
        for source_obj in sources:
            response = requests.request('GET', source_obj.link)
            if response.status_code != 200:
                return 'Invalid response'

            source_method = methods.get(source_obj.method)
            if source_method:
                source_method(source_obj, response)
            else:
                return 'Invalid method'


@shared_task
def testing():
    return 'TESTING'
