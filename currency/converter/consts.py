from converter.utils import ECBMethod, CBRFMethod

AUTOLOAD_METHOD_CHOICES = [
    ('get_cbr_data', 'get_cbr_data'),
    ('get_ecb_data', 'get_ecb_data'),
]

METHODS = {
        'get_cbr_data': CBRFMethod,
        'get_ecb_data': ECBMethod,
    }
