from converter.methods import ECBMethod, CBRMethod

AUTOLOAD_METHOD_CHOICES = [
    ('get_cbr_data', 'get_cbr_data'),
    ('get_ecb_data', 'get_ecb_data'),
]

METHODS = {
        'get_cbr_data': CBRMethod,
        'get_ecb_data': ECBMethod,
    }
