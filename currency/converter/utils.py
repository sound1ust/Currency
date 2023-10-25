import json
from datetime import datetime
from decimal import Decimal


class ConverterJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj).__name__ in ('Source', 'User'):
            return obj.id

        if isinstance(obj, (datetime, Decimal)):
            return str(obj)

        return super().default(obj)


def exc_raiser(exc):
    def decor(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception:
                raise exc
            else:
                return result

        return wrapper

    return decor
