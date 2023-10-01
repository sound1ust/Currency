from celery import shared_task

from requests.exceptions import RequestException

from converter.exceptions import CurrencyBaseException
from converter.models import Converter, User, Source
from converter.consts import METHODS
from django.utils import timezone


@shared_task
def get_currency_scheduler():
    active_source_types = Source.objects.filter(is_active=True)
    if active_source_types:
        for source in active_source_types:
            get_currency.apply_async(args=(source.id,))


@shared_task
def get_currency(source_id):
    def create_convertors(resp):
        for ticker in resp.keys():
            ticker_data = resp.get(ticker)
            converter = Converter(**ticker_data)

            converter_exists = Converter.objects.filter(
                source_id=source_id,
                input_ticker=converter.input_ticker,
                output_ticker=converter.output_ticker,
            ).order_by('created_at')

            if not converter_exists:
                converter.save()
            else:
                last_converter = converter_exists.last()
                if last_converter.value == converter.value:
                    return None
                else:
                    converter.save()

    source = Source.objects.filter(id=source_id).first()
    if source:
        try:
            method = METHODS.get(source.autoload_method)(
                source,
                source.tickers,
                source.base_ticker,
                User.objects.all().first(),
            )
            response = method.make_request()
        except RequestException as exc:
            if hasattr(exc, 'response'):
                response = {exc.response.status_code: exc.response.reason}
            else:
                response = {500: 'Connection Error'}
        except CurrencyBaseException as exc:
            response = {exc.code: exc.message}
        else:
            create_convertors(response)

        # source.last_run_result = response
        # source.last_time_run = timezone.now()
        # source.save()


@shared_task
def testing():
    return 'TESTING'
