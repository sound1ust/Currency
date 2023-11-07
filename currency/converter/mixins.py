from json import loads

from converter.exceptions import ExchangeInfoErrorException
from converter.exceptions import SourceDateNotFoundException
from requests import request


class BinanceMixin:
    def get_exchange_info(self):
        exchange_info = {}

        raw_response = request(
            'GET',
            'https://api.binance.com/api/v3/exchangeInfo',
        )
        raw_response.raise_for_status()

        response = loads(raw_response.content.decode('utf-8'))

        symbols = response.get('symbols')
        if not symbols:
            raise ExchangeInfoErrorException(
                'Binance exchange info is invalid',
            )

        exchange_info['server_time'] = self.get_server_time(response)

        for symbol in symbols:
            symbol_name = symbol.get('symbol')
            exchange_info[symbol_name] = {}
            exchange_info[symbol_name]['input_ticker'] = symbol.get(
                'baseAsset',
            )
            exchange_info[symbol_name]['output_ticker'] = symbol.get(
                'quoteAsset',
            )

        return exchange_info

    def get_server_time(self, response):
        server_time = response.get('serverTime')

        if not server_time:
            raise SourceDateNotFoundException(
                'Binance server time not found',
            )
        return server_time
