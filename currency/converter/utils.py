import xmltodict
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

from converter.exceptions import CurrencyNotFoundException
from converter.models import Converter, User
from requests import request


class BaseMethod(ABC):
    def __init__(self, tickers, base_currency):
        self.base_currency = base_currency
        self.request_type = 'GET'
        self.tickers = tickers
        self.url = ''

    def prepare_request(self):
        request_data = {
            'method': self.request_type,
            'url': self.url
        }
        return request_data

    def make_request(self):
        raw_response = request(**self.prepare_request())
        raw_response.raise_for_status()
        response = self.handle_response(raw_response)
        return response

    @abstractmethod
    def handle_response(self, response):
        if not response:
            raise CurrencyNotFoundException


class CBRFMethod(BaseMethod):
    def __init__(self, tickers, base_currency):
        super().__init__(tickers, base_currency)
        self.url = 'https://cbrf'
        self.base_currency = self.base_currency or 'RUB'

    def handle_response(self, response):
        pass


class ECBMethod(BaseMethod):
    def __init__(self, tickers, base_currency):
        super().__init__(tickers, base_currency)
        self.url = 'https://ecb'
        self.base_currency = self.base_currency or 'EUR'

    def handle_response(self, response):
        pass


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
