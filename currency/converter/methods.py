from xmltodict import parse
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from converter.utils import exc_raiser
from converter.exceptions import CurrencyBaseException
from requests import request


class BaseMethod(ABC):
    def __init__(self, source_obj, tickers, base_ticker, user):
        self.source_obj = source_obj
        self.tickers = tickers
        self.base_ticker = base_ticker
        self.user = user
        self.request_type = 'GET'
        self.url = ''

    def prepare_request(self):
        request_data = {
            'method': self.request_type,
            'url': self.url
        }
        return request_data

    @exc_raiser(CurrencyBaseException)
    def make_request(self):
        raw_response = request(**self.prepare_request())
        raw_response.raise_for_status()
        response = self.handle_response(raw_response)
        return response

    @abstractmethod
    def handle_response(self, response):
        pass


class CBRMethod(BaseMethod):
    def __init__(self, source_obj, tickers, base_ticker, user):
        super().__init__(source_obj, tickers, base_ticker, user)
        self.url = 'https://www.cbr.ru/scripts/XML_daily.asp'
        self.base_ticker = self.base_ticker or 'RUB'

    def handle_response(self, raw_response):
        currency_data = parse(raw_response.content).get('ValCurs')
        response = {}

        for ticker in self.tickers:
            ticker_data = next((el for el in currency_data.get('Valute') if
                                el.get('CharCode') == ticker))

            input_ticker = ticker

            output_ticker = self.base_ticker

            value = ticker_data.get('Value')
            value = float(value.replace(',', '.'))

            coefficient = int(ticker_data.get('Nominal'))

            source_id = self.source_obj

            source_date = datetime.strptime(
                currency_data.get('@Date'), '%d.%m.%Y'
            ) + timedelta(hours=1)

            updated_by = self.user

            response[ticker] = {
                'input_ticker': input_ticker,
                'output_ticker': output_ticker,
                'value': value,
                'coefficient': coefficient,
                'source_id': source_id,
                'source_date': source_date,
                'updated_by': updated_by,
            }

        return response


class ECBMethod(BaseMethod):
    def __init__(self, source_obj, tickers, base_ticker, user):
        super().__init__(source_obj, tickers, base_ticker, user)
        self.url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
        self.base_ticker = self.base_ticker or 'EUR'

    def handle_response(self, response):
        pass
