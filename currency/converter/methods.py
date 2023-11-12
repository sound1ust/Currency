from abc import ABC
from abc import abstractmethod
from datetime import datetime
from decimal import Decimal
from json import loads

from converter.exceptions import CurrencyNotFoundException
from converter.exceptions import ExchangeInfoInputTickerNotFoundException
from converter.exceptions import ExchangeInfoOutputTickerNotFoundException
from converter.exceptions import SourceDateNotFoundException
from converter.exceptions import TickerCoefficientNotFoundException
from converter.exceptions import TickerDataNotFoundException
from converter.exceptions import TickerNotFoundException
from converter.exceptions import TickerValueNotFoundException
from converter.mixins import BinanceMixin
from requests import request
from xmltodict import parse


class BaseMethod(ABC):
    """Abstract class of method that provides retrieving
    currency data from different banks API.
    """

    def __init__(self, source_obj, tickers, base_ticker, user):
        self.source_obj = source_obj
        self.tickers = tickers
        self.base_ticker = base_ticker
        self.user = user
        self.request_type = 'GET'
        self.url = ''
        self.single_request = True

    def prepare_request(self) -> dict:
        """Preparing request data before making request."""
        request_data = {
            'method': self.request_type,
            'url': self.url,
        }

        return request_data

    def make_request(self) -> dict:
        """Depending on single_request field calls
        single or multiple requests function.
        """
        if self.single_request:
            return self.make_single_request()
        else:
            return self.make_multiple_requests()

    def make_single_request(self) -> dict:
        """Makes single request for a data, checks it status and
        calls a function to handle the hole response at once"""
        raw_response = request(**self.prepare_request())
        raw_response.raise_for_status()
        response = self.handle_response(raw_response)
        return response

    def make_multiple_requests(self) -> dict:
        """Makes multiple requests for a data, checks them statuses and
        calls a function to handle an every single response"""
        response = {}

        for ticker in self.tickers:
            if not ticker:
                raise TickerNotFoundException(
                    f'No tickers found in {self.source_obj.name} source',
                )

            self.base_ticker = ticker
            raw_response = request(**self.prepare_request())
            raw_response.raise_for_status()
            response[ticker] = self.handle_single_response(
                raw_response,
                ticker,
            )

        return response

    def handle_response(self, raw_response):
        """Handling response for an every ticker in tickers field."""
        response = {}

        for ticker in self.tickers:
            if not ticker:
                raise TickerNotFoundException(
                    f'No tickers found in {self.source_obj.name} source',
                )

            response[ticker] = self.handle_single_response(
                raw_response,
                ticker,
            )

        return response

    def handle_single_response(self, raw_response, ticker):
        """Handling response for a single ticker that passed to function"""
        input_ticker = ticker
        output_ticker = self.base_ticker
        currency_data = self.get_currency_data(raw_response)
        ticker_data = self.get_ticker_data(currency_data, ticker)
        value = self.get_value(ticker_data, ticker)
        coefficient = self.get_coefficient(ticker_data, ticker)
        source_id = self.source_obj.id
        source_date = self.get_source_date(currency_data, ticker_data)
        updated_by = self.user.id

        return {
            'input_ticker': input_ticker,
            'output_ticker': output_ticker,
            'value': value,
            'coefficient': coefficient,
            'source_id': source_id,
            'source_date': source_date,
            'updated_by': updated_by,
        }

    @staticmethod
    def handle_data(data, exc, error_message):
        """Checks out if incoming data exists and raise an exception
        with a message that are passed into function.

        Args:
        data: The incoming data to check.
        exc: The exception to raise if data does not exist.
        error_message: The error message for the exception.

        Raises:
        exc: If data does not exist.

        Returns:
        The incoming data if it exists.
        """
        if not data:
            raise exc(error_message)

        return data

    @abstractmethod
    def get_currency_data(self, raw_response):
        pass

    def get_ticker_data(self, currency_data, ticker):
        pass

    def get_value(self, ticker_data, ticker):
        pass

    def get_coefficient(self, ticker_data, ticker):
        pass

    def get_source_date(self, currency_data, ticker_data):
        pass


class CBRMethod(BaseMethod):
    """BaseMethod implementation working with the API of the
    Central Bank of the Russian Federation.
    """

    def __init__(self, source_obj, tickers, base_ticker, user):
        super().__init__(source_obj, tickers, base_ticker, user)
        self.url = 'https://www.cbr.ru/scripts/XML_daily.asp'
        self.base_ticker = self.base_ticker or 'RUB'

    def get_currency_data(self, raw_response):
        currency_data = parse(raw_response.content).get('ValCurs')

        return self.handle_data(
            currency_data,
            CurrencyNotFoundException,
            f'Invalid currency data from {self.source_obj.name} source',
        )

    def get_ticker_data(self, currency_data, ticker):
        try:
            ticker_data = next(
                (
                    el
                    for el in currency_data.get('Valute')
                    if el.get('CharCode') == ticker
                )
            )
        except StopIteration:
            ticker_data = None

        return self.handle_data(
            ticker_data,
            TickerDataNotFoundException,
            f'No data found for ticker {ticker}',
        )

    def get_value(self, ticker_data, ticker):
        value = Decimal(ticker_data.get('Value').replace(',', '.'))

        return self.handle_data(
            value,
            TickerValueNotFoundException,
            f'{ticker} value not found',
        )

    def get_coefficient(self, ticker_data, ticker):
        coefficient = int(ticker_data.get('Nominal'))

        return self.handle_data(
            coefficient,
            TickerCoefficientNotFoundException,
            f'{ticker} coefficient not found',
        )

    def get_source_date(self, currency_data, ticker_data):
        source_date = datetime.strptime(
            currency_data.get('@Date'),
            '%d.%m.%Y',
        )

        return self.handle_data(
            source_date,
            SourceDateNotFoundException,
            f"Source '{self.source_obj.name}' date not found",
        )


class ECBMethod(BaseMethod):
    """BaseMethod implementation working with the API of the
    European Central Bank.
    """

    def __init__(self, source_obj, tickers, base_ticker, user):
        super().__init__(source_obj, tickers, base_ticker, user)
        self.url = (
            'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
        )
        self.base_ticker = self.base_ticker or 'EUR'

    def get_currency_data(self, raw_response):
        currency_data = (
            parse(
                raw_response.content,
            )
            .get('gesmes:Envelope')
            .get('Cube')
            .get('Cube')
        )

        return self.handle_data(
            currency_data,
            CurrencyNotFoundException,
            f'Invalid currency data from {self.source_obj.name} source',
        )

    def get_ticker_data(self, currency_data, ticker):
        ticker_data = next(
            (
                el
                for el in currency_data.get('Cube')
                if el.get('@currency') == ticker
            )
        )

        return self.handle_data(
            ticker_data,
            TickerDataNotFoundException,
            f'No data found for ticker {ticker}',
        )

    def get_value(self, ticker_data, ticker):
        value = Decimal(ticker_data.get('@rate'))

        return self.handle_data(
            value,
            TickerValueNotFoundException,
            f'{ticker} value not found',
        )

    def get_coefficient(self, ticker_data, ticker):
        coefficient = 1

        return coefficient

    def get_source_date(self, currency_data, ticker_data):
        source_date = datetime.strptime(
            currency_data.get('@time'),
            '%Y-%m-%d',
        )

        return self.handle_data(
            source_date,
            SourceDateNotFoundException,
            f"Source '{self.source_obj.name}' date not found",
        )


class NBRBMethod(BaseMethod):
    """BaseMethod implementation working with the API of the
    National Bank of the Republic of Belarus.
    """

    def __init__(self, source_obj, tickers, base_ticker, user):
        super().__init__(source_obj, tickers, base_ticker, user)
        self.url = 'https://api.nbrb.by/exrates/rates?periodicity=0'
        self.base_ticker = base_ticker or 'BYN'

    def get_currency_data(self, raw_response):
        currency_data = loads(raw_response.content)

        return self.handle_data(
            currency_data,
            CurrencyNotFoundException,
            f'Invalid currency data from {self.source_obj.name} source',
        )

    def get_ticker_data(self, currency_data, ticker):
        ticker_data = next(
            (
                el
                for el in currency_data
                if el.get('Cur_Abbreviation') == ticker
            )
        )

        return self.handle_data(
            ticker_data,
            TickerDataNotFoundException,
            f'No data found for ticker {ticker}',
        )

    def get_value(self, ticker_data, ticker):
        value = ticker_data.get('Cur_OfficialRate')

        return self.handle_data(
            value,
            TickerValueNotFoundException,
            f'{ticker} value not found',
        )

    def get_coefficient(self, ticker_data, ticker):
        coefficient = ticker_data.get('Cur_Scale')

        return self.handle_data(
            coefficient,
            TickerCoefficientNotFoundException,
            f'{ticker} coefficient not found',
        )

    def get_source_date(self, currency_data, ticker_data):
        source_date = datetime.strptime(
            ticker_data.get('Date'),
            '%Y-%m-%dT%H:%M:%S',
        )

        return self.handle_data(
            source_date,
            SourceDateNotFoundException,
            f"Source '{self.source_obj.name}' date not found",
        )


class BinanceSingleMethod(BinanceMixin, BaseMethod):
    """BaseMethod implementation working with the API of the
    Binance. Also inherited from BinanceMixin.
    """

    def __init__(self, source_obj, tickers, base_ticker, user):
        super().__init__(source_obj, tickers, base_ticker, user)
        self.url = 'https://api.binance.com/api/v3/avgPrice?symbol='
        self.base_ticker = None
        self.exchange_info = self.get_exchange_info()
        self.single_request = False

    def prepare_request(self):
        request_data = {
            'method': self.request_type,
            'url': self.url + self.base_ticker,
        }

        return request_data

    def handle_single_response(self, raw_response, ticker):
        input_ticker = self.get_input_ticker(ticker)
        output_ticker = self.get_output_ticker(ticker)
        currency_data = self.get_currency_data(raw_response)
        value = self.get_value(currency_data, ticker)
        coefficient = 1
        source_id = self.source_obj.id
        source_date = self.get_source_date()
        updated_by = self.user.id

        return {
            'input_ticker': input_ticker,
            'output_ticker': output_ticker,
            'value': value,
            'coefficient': coefficient,
            'source_id': source_id,
            'source_date': source_date,
            'updated_by': updated_by,
        }

    def get_input_ticker(self, ticker):
        input_ticker = self.exchange_info[ticker]['input_ticker']

        return self.handle_data(
            input_ticker,
            ExchangeInfoInputTickerNotFoundException,
            f'Input ticker is not found in exchange data of '
            f'{self.source_obj.name} source',
        )

    def get_output_ticker(self, ticker):
        output_ticker = self.exchange_info[ticker]['output_ticker']

        return self.handle_data(
            output_ticker,
            ExchangeInfoOutputTickerNotFoundException,
            f'Output ticker is not found in exchange data of '
            f'{self.source_obj.name} source',
        )

    def get_currency_data(self, raw_response):
        currency_data = loads(raw_response.content)

        return self.handle_data(
            currency_data,
            CurrencyNotFoundException,
            f'Invalid currency data from {self.source_obj.name} source',
        )

    def get_value(self, currency_data, ticker):
        value = Decimal(currency_data.get('price'))

        return self.handle_data(
            value,
            TickerValueNotFoundException,
            f'{ticker} value not found',
        )

    def get_source_date(self):
        server_time = self.exchange_info.get('server_time')

        try:
            source_date = datetime.fromtimestamp(
                server_time / 1000.0,
            )
        except TypeError:
            raise SourceDateNotFoundException(
                f"Source '{self.source_obj.name}' date must be timestamp",
            )
        else:
            return source_date
