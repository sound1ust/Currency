class CurrencyBaseException(Exception):
    code = 0
    base_message = 'Unknown Exception'

    def __init__(self, message=None):
        self.message = message if message is not None else self.base_message


class CurrencyNotFoundException(CurrencyBaseException):
    code = 700
    base_message = 'Currency Not Found'


class CurrencyNotChangeException(CurrencyBaseException):
    code = 701
    base_message = "Currency didn't change"


class TickerNotFoundException(CurrencyBaseException):
    code = 800
    base_message = 'Ticker not found'


class TickerDataNotFoundException(CurrencyBaseException):
    code = 801
    base_message = 'Ticker data not found'


class TickerValueNotFoundException(CurrencyBaseException):
    code = 802
    base_message = 'Ticker value not found'


class TickerCoefficientNotFoundException(CurrencyBaseException):
    code = 803
    base_message = 'Ticker coefficient not found'


class SourceDateNotFoundException(CurrencyBaseException):
    code = 900
    base_message = 'Source date not found'


class NoActiveSourcesException(CurrencyBaseException):
    code = 901
    base_message = 'No active sources found'


class SourceDateInvalidException(CurrencyBaseException):
    code = 902
    base_message = 'Source date is invalid'


class ValidationErrorException(CurrencyBaseException):
    code = 1000
    base_message = 'Validation Error'


class ExchangeInfoErrorException(CurrencyBaseException):
    code = 1100
    base_message = 'Invalid exchange info'


class ExcahngeSymbolNotFoundException(CurrencyBaseException):
    code = 1101
    base_message = 'Symbol not found'


class ExchangeInfoInputTickerNotFoundException(CurrencyBaseException):
    code = 1102
    base_message = 'Input ticker not found'


class ExchangeInfoOutputTickerNotFoundException(CurrencyBaseException):
    code = 1103
    base_message = 'Output ticker not found'
