from xmltodict import parse
from json import loads
from datetime import datetime
from abc import ABC, abstractmethod
from converter.exceptions import *
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
            'url': self.url,
        }
        return request_data

    def make_request(self):
        raw_response = request(**self.prepare_request())
        raw_response.raise_for_status()
        response = self.handle_response(raw_response)
        return response

    @abstractmethod
    def handle_response(self, raw_response):
        pass


class CBRMethod(BaseMethod):
    def __init__(self, source_obj, tickers, base_ticker, user):
        super().__init__(source_obj, tickers, base_ticker, user)
        self.url = 'https://www.cbr.ru/scripts/XML_daily.asp'
        self.base_ticker = self.base_ticker or 'RUB'

    def handle_response(self, raw_response):
        currency_data = parse(raw_response.content).get('ValCurs')
        if not currency_data:
            raise CurrencyNotFoundException

        response = {}

        for ticker in self.tickers:
            if not ticker:
                raise TickerNotFoundException

            ticker_data = next((el for el in currency_data.get('Valute') if
                                el.get('CharCode') == ticker))
            if not ticker_data:
                raise TickerDataNotFoundException(
                    f"No data found for ticker {ticker}"
                )

            input_ticker = ticker

            output_ticker = self.base_ticker

            value = ticker_data.get('Value')
            if not value:
                raise TickerValueNotFoundException(
                    f"{ticker} value not found"
                )
            value = float(value.replace(',', '.'))

            coefficient = int(ticker_data.get('Nominal'))
            if not coefficient:
                raise TickerCoefficientNotFoundException(
                    f"{ticker} coefficient not found"
                )

            source_id = self.source_obj.id

            source_date = datetime.strptime(
                currency_data.get('@Date'), '%d.%m.%Y'
            )
            if not source_date:
                raise SourceDateNotFoundException(
                    f"Source '{self.source_obj.name}' date not found"
                )

            updated_by = self.user.id

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

    def handle_response(self, raw_response):
        currency_data = parse(
            raw_response.content
        ).get('gesmes:Envelope').get('Cube').get('Cube')
        if not currency_data:
            raise CurrencyNotFoundException

        response = {}

        for ticker in self.tickers:
            if not ticker:
                raise TickerNotFoundException

            ticker_data = next((el for el in currency_data.get('Cube') if
                                el.get('@currency') == ticker))
            if not ticker_data:
                raise TickerDataNotFoundException(
                    f"No data found for ticker {ticker}"
                )

            input_ticker = ticker

            output_ticker = self.base_ticker

            value = float(ticker_data.get('@rate'))
            if not value:
                raise TickerValueNotFoundException(
                    f"{ticker} value not found"
                )

            coefficient = 1

            source_id = self.source_obj.id

            source_date = datetime.strptime(
                currency_data.get('@time'), '%Y-%m-%d'
            )
            if not source_date:
                raise SourceDateNotFoundException(
                    f"Source '{self.source_obj.name}' date not found"
                )

            updated_by = self.user.id

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


class NBRBMethod(BaseMethod):
    def __init__(self, source_obj, tickers, base_ticker, user):
        super().__init__(source_obj, tickers, base_ticker, user)
        self.url = 'https://api.nbrb.by/exrates/rates?periodicity=0'
        self.base_ticker = base_ticker or 'BYN'

    def handle_response(self, raw_response):
        currency_data = loads(raw_response.content)
        if not currency_data:
            raise CurrencyNotFoundException

        response = {}

        for ticker in self.tickers:
            if not ticker:
                raise TickerNotFoundException

            ticker_data = next((el for el in currency_data if
                                el.get('Cur_Abbreviation') == ticker))
            if not ticker_data:
                raise TickerDataNotFoundException(
                    f"No data found for ticker {ticker}"
                )

            input_ticker = ticker

            output_ticker = self.base_ticker

            value = ticker_data.get('Cur_OfficialRate')
            if not value:
                raise TickerValueNotFoundException(
                    f"{ticker} value not found"
                )

            coefficient = ticker_data.get('Cur_Scale')
            if not coefficient:
                raise TickerCoefficientNotFoundException(
                    f"{ticker} coefficient not found"
                )

            source_id = self.source_obj.id

            source_date = datetime.strptime(
                ticker_data.get('Date'), '%Y-%m-%dT%H:%M:%S'
            )
            if not source_date:
                raise SourceDateNotFoundException(
                    f"Source '{self.source_obj.name}' date not found"
                )

            updated_by = self.user.id

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
