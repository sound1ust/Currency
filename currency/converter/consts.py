from converter.methods import ECBMethod, CBRMethod, NBRBMethod, \
    BinanceSingleMethod

AUTOLOAD_METHOD_CHOICES = [
    ('get_cbr_data', 'get_cbr_data'),
    ('get_ecb_data', 'get_ecb_data'),
    ('get_nbrb_data', 'get_nbrb_data'),
    ('get_binance_data', 'get_binance_data'),
]

METHODS = {
        'get_cbr_data': CBRMethod,
        'get_ecb_data': ECBMethod,
        'get_nbrb_data': NBRBMethod,
        'get_binance_data': BinanceSingleMethod,
    }
