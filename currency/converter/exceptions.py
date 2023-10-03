class CurrencyBaseException(Exception):
    code = 0
    message = 'Unknown Exception'


class CurrencyNotFoundException(CurrencyBaseException):
    code = 700
    message = 'Currency Not Found'


class CurrencyNotChangeException(CurrencyBaseException):
    code = 701
    message = "Currency didn't change"


class TickerNotFoundException(CurrencyBaseException):
    code = 800
    message = 'Ticker not found'


class TickerDataNotFoundException(CurrencyBaseException):
    code = 801
    message = "Ticker data not found"


class TickerValueNotFoundException(CurrencyBaseException):
    code = 802
    message = 'Ticker value not found'


class TickerCoefficientNotFoundException(CurrencyBaseException):
    code = 803
    message = 'Ticker coefficient not found'


class SourceDateNotFoundException(CurrencyBaseException):
    code = 900
    message = 'Source date not found'


class NoActiveSourcesException(CurrencyBaseException):
    code = 901
    message = 'No active sources found'


class ValidationErrorException(CurrencyBaseException):
    code = 1000
    message = 'Validation Error'
