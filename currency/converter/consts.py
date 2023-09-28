from converter.utils import get_ecb_data, get_cbr_data

AUTOLOAD_METHOD_CHOICES = [
    ('get_cbr_data', 'get_cbr_data'),
    ('get_ecb_data', 'get_ecb_data'),
]

METHODS = {
        'get_cbr_data': get_cbr_data,
        'get_ecb_data': get_ecb_data,
    }
