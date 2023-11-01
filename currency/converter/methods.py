from datetime import datetime
from abc import ABC, abstractmethod
from json import loads
from decimal import Decimal

from xmltodict import parse
from requests import request

from converter.exceptions import *


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
            'url': self.url,
        }
        return request_data

    def make_request(self):
        raw_response = request(**self.prepare_request())
        raw_response.raise_for_status()
        response = self.handle_response(raw_response)
        return response

    def handle_response(self, raw_response):
        response = {}

        for ticker in self.tickers:
            if not ticker:
                raise TickerNotFoundException(
                    f"No tickers found in {self.source_obj.name} source"
                )

            response[ticker] = self.handle_single_response(
                raw_response, ticker
            )

        return response

    def handle_single_response(self, raw_response, ticker):
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
        if not data:
            raise exc(error_message)

        return data

    @abstractmethod
    def get_currency_data(self, raw_response):
        pass

    @abstractmethod
    def get_ticker_data(self, currency_data, ticker):
        pass

    @abstractmethod
    def get_value(self, ticker_data, ticker):
        pass

    @abstractmethod
    def get_coefficient(self, ticker_data, ticker):
        pass

    @abstractmethod
    def get_source_date(self, currency_data, ticker_data):
        pass


class CBRMethod(BaseMethod):
    def __init__(self, source_obj, tickers, base_ticker, user):
        super().__init__(source_obj, tickers, base_ticker, user)
        self.url = 'https://www.cbr.ru/scripts/XML_daily.asp'
        self.base_ticker = self.base_ticker or 'RUB'

    def get_currency_data(self, raw_response):
        currency_data = parse(raw_response.content).get('ValCurs')

        return self.handle_data(
            currency_data, CurrencyNotFoundException,
            f"Invalid currency data from {self.source_obj.name} source"
        )

    def get_ticker_data(self, currency_data, ticker):
        ticker_data = next((el for el in currency_data.get('Valute') if
                            el.get('CharCode') == ticker))

        return self.handle_data(
            ticker_data, TickerDataNotFoundException,
            f"No data found for ticker {ticker}"
        )

    def get_value(self, ticker_data, ticker):
        value = Decimal(ticker_data.get('Value').replace(',', '.'))

        return self.handle_data(
            value, TickerValueNotFoundException,
            f"{ticker} value not found"
        )

    def get_coefficient(self, ticker_data, ticker):
        coefficient = int(ticker_data.get('Nominal'))

        return self.handle_data(
            coefficient, TickerCoefficientNotFoundException,
            f"{ticker} coefficient not found"
        )

    def get_source_date(self, currency_data, ticker_data):
        source_date = datetime.strptime(
            currency_data.get('@Date'), '%d.%m.%Y'
        )

        return self.handle_data(
            source_date, SourceDateNotFoundException,
            f"Source '{self.source_obj.name}' date not found"
        )


class ECBMethod(BaseMethod):
    def __init__(self, source_obj, tickers, base_ticker, user):
        super().__init__(source_obj, tickers, base_ticker, user)
        self.url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
        self.base_ticker = self.base_ticker or 'EUR'

    def get_currency_data(self, raw_response):
        currency_data = parse(
            raw_response.content
        ).get('gesmes:Envelope').get('Cube').get('Cube')

        return self.handle_data(
            currency_data, CurrencyNotFoundException,
            f"Invalid currency data from {self.source_obj.name} source"
        )

    def get_ticker_data(self, currency_data, ticker):
        ticker_data = next((el for el in currency_data.get('Cube') if
                            el.get('@currency') == ticker))

        return self.handle_data(
            ticker_data, TickerDataNotFoundException,
            f"No data found for ticker {ticker}"
        )

    def get_value(self, ticker_data, ticker):
        value = Decimal(ticker_data.get('@rate'))

        return self.handle_data(
            value, TickerValueNotFoundException,
             f"{ticker} value not found"
        )

    def get_coefficient(self, ticker_data, ticker):
        coefficient = 1

        return coefficient

    def get_source_date(self, currency_data, ticker_data):
        source_date = datetime.strptime(
            currency_data.get('@time'), '%Y-%m-%d'
        )

        return self.handle_data(
            source_date, SourceDateNotFoundException,
            f"Source '{self.source_obj.name}' date not found"
        )


class NBRBMethod(BaseMethod):
    def __init__(self, source_obj, tickers, base_ticker, user):
        super().__init__(source_obj, tickers, base_ticker, user)
        self.url = 'https://api.nbrb.by/exrates/rates?periodicity=0'
        self.base_ticker = base_ticker or 'BYN'

    def get_currency_data(self, raw_response):
        currency_data = loads(raw_response.content)

        return self.handle_data(
            currency_data, CurrencyNotFoundException,
            f"Invalid currency data from {self.source_obj.name} source"
        )

    def get_ticker_data(self, currency_data, ticker):
        ticker_data = next((el for el in currency_data if
                            el.get('Cur_Abbreviation') == ticker))

        return self.handle_data(
            ticker_data, TickerDataNotFoundException,
            f"No data found for ticker {ticker}"
        )

    def get_value(self, ticker_data, ticker):
        value = ticker_data.get('Cur_OfficialRate')

        return self.handle_data(
            value, TickerValueNotFoundException,
             f"{ticker} value not found"
        )

    def get_coefficient(self, ticker_data, ticker):
        coefficient = ticker_data.get('Cur_Scale')

        return self.handle_data(
            coefficient, TickerCoefficientNotFoundException,
            f"{ticker} coefficient not found"
        )

    def get_source_date(self, currency_data, ticker_data):
        source_date = datetime.strptime(
            ticker_data.get('Date'), '%Y-%m-%dT%H:%M:%S'
        )

        return self.handle_data(
            source_date, SourceDateNotFoundException,
            f"Source '{self.source_obj.name}' date not found"
        )


class BinanceSingleMethod(BaseMethod):
    def __init__(self, source_obj, tickers, base_ticker, user):
        super().__init__(source_obj, tickers, base_ticker, user)
        self.url = 'https://api.binance.com/api/v3/avgPrice?symbol='
        self.base_ticker = self.base_ticker or 'BTC'
        self.current_ticker = None
        self.exchange_info = self.get_exchange_info()

    def prepare_request(self):
        request_data = {
            'method': self.request_type,
            'url': self.url + self.current_ticker,
        }

        return request_data

    def make_request(self):
        response = {}

        for ticker in self.tickers:
            if not ticker:
                raise TickerNotFoundException(
                    f"No tickers found in {self.source_obj.name} source"
                )

            self.current_ticker = ticker + self.base_ticker
            raw_response = request(**self.prepare_request())
            raw_response.raise_for_status()
            response[ticker] = self.handle_single_response(
                raw_response, ticker
            )

        return response

    def get_currency_data(self, raw_response):
        currency_data = loads(raw_response.content)

        return self.handle_data(
            currency_data, CurrencyNotFoundException,
            f"Invalid currency data from {self.source_obj.name} source"
        )

    def get_ticker_data(self, currency_data, ticker):
        return currency_data

    def get_value(self, ticker_data, ticker):
        value = Decimal(ticker_data.get('price'))

        return self.handle_data(
            value, TickerValueNotFoundException,
            f"{ticker} value not found"
        )

    def get_coefficient(self, ticker_data, ticker):
        coefficient = 1

        return coefficient

    def get_source_date(self, currency_data, ticker_data):
        server_time = self.exchange_info.get('server_time')

        try:
            source_date = datetime.fromtimestamp(
                server_time / 1000.0
            )
        except TypeError:
            raise SourceDateNotFoundException(
                f"Source '{self.source_obj.name}' date must be timestamp"
            )
        else:
            return source_date

    def get_exchange_info(self):
        exchange_info = {}

        raw_response = request(
            'GET', 'https://api.binance.com/api/v3/exchangeInfo'
        )
        raw_response.raise_for_status()

        response = loads(raw_response.content.decode('utf-8'))

        symbols = response.get('symbols')
        self.handle_data(
            symbols, ExchangeInfoErrorException,
            f"Source '{self.source_obj.name}' exchange info is invalid"
        )

        exchange_info['server_time'] = self.get_server_time(response)

        for symbol in symbols:
            sym = symbol.get('symbol')
            exchange_info[sym] = {}
            exchange_info[sym]['input_ticker'] = symbol.get('baseAsset')
            exchange_info[sym]['output_ticker'] = symbol.get('quoteAsset')

        return exchange_info

    def get_server_time(self, response):
        server_time = response.get('serverTime')

        return self.handle_data(
            server_time, SourceDateNotFoundException,
            f"Source '{self.source_obj.name}' server time not found"
        )
