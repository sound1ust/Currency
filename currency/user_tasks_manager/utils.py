from datetime import datetime
from decimal import Decimal


def format_result_name(name: str, dt: datetime) -> str:
    formatted_name = '_'.join(name.split())
    formatted_dt = ''.join(
        str(dt).replace(' ', '').replace('-', '').replace('.', '').split(':'),
    )

    return formatted_name + '_' + formatted_dt


def format_start_parameters(data: dict) -> str:
    formatted_data = ''
    for key, value in data.items():
        if key == 'created_at__gte':
            formatted_data += f'From {str(value)}.\n'
        if key == 'created_at__lte':
            formatted_data += f'To {str(value)}.\n'
        if key == 'input_ticker__in':
            formatted_data += f'Input tickers: {str(value)}.\n'
        if key == 'output_ticker__in':
            formatted_data += f'Output tickers: {str(value)}.\n'
        if key == 'value__gte':
            formatted_data += f'Value from: {str(value)}.\n'
        if key == 'value__lte':
            formatted_data += f'Value to: {str(value)}.\n'
        if key == 'output_ticker__in':
            formatted_data += f'Output tickers: {str(value)}.\n'
        if key == 'source_id__in':
            formatted_data += (
                f'From sources: ' f"{', '.join([str(i) for i in value])}.\n"
            )
        if key == 'updated_by__in':
            formatted_data += (
                f'Updated by: ' f"{', '.join([str(i) for i in value])}.\n"
            )

    return formatted_data


def normalize_decimal(num: Decimal) -> Decimal:
    return num.quantize(Decimal('.00001')).normalize()
