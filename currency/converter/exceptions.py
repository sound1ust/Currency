class CurrencyBaseException(Exception):
    code = 0
    message = 'Unknown Exception'


class CurrencyNotFoundException(CurrencyBaseException):
    code = 700
    message = 'Currency Not Found'
