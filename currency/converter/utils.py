import json
from datetime import datetime
from decimal import Decimal
from hashlib import md5


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


def get_dict_key(data: dict) -> str:
    """
    This code will sort the dictionary, serialize it to a JSON string,
    generate an MD5 hash of the string and then converts binary hash value
    into a hexadecimal string.
    """
    sorted_data = json.dumps(data, sort_keys=True)
    key = md5(sorted_data.encode()).hexdigest()

    return key
