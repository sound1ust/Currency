from datetime import datetime
from functools import wraps
from json import dumps
from logging import getLogger

from celery import shared_task
from converter.consts import METHODS
from converter.exceptions import CurrencyBaseException
from converter.exceptions import CurrencyNotChangeException
from converter.exceptions import NoActiveSourcesException
from converter.exceptions import ValidationErrorException
from converter.forms import ConverterForm
from converter.models import Converter
from converter.models import Source
from converter.models import User
from converter.utils import ConverterJSONEncoder
from converter.utils import exc_raiser
from requests.exceptions import RequestException


logger = getLogger('currency_converter')


def task_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            logger.error(f'Error: {func.__name__}: {exc}')
        else:
            logger.info(f'Info: {func.__name__}: {result}')
            return result

    return wrapper


@shared_task
def get_currency_scheduler():
    active_source_types = Source.objects.filter(is_active=True)
    if active_source_types:
        for source in active_source_types:
            get_currency.apply_async(args=(source.id,))
    else:
        raise NoActiveSourcesException  # Stopping if there is no active srcs


@shared_task
@task_logger
@exc_raiser(CurrencyBaseException)
def get_currency(source_id):
    def create_convertors(resp):
        for ticker in resp.keys():
            ticker_data = resp.get(ticker)
            form = ConverterForm(data=ticker_data)
            if form.is_valid():
                converter = form.save(commit=False)  # No saving for now
            else:
                raise ValidationErrorException(
                    f'Validation error(s) for ticker {ticker}: {form.errors}',
                )

            converter_exists = Converter.objects.filter(
                source_id=source_id,
                input_ticker=converter.input_ticker,
                output_ticker=converter.output_ticker,
            ).order_by('created_at')

            if (
                not converter_exists
                or converter_exists.last().value != converter.value
            ):
                converter.save()  # Now save
            else:
                raise CurrencyNotChangeException(
                    f'Currency for {converter.input_ticker}/'
                    f"{converter.output_ticker} didn't change",
                )

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
        except Exception as e:
            response = {'error': str(e)}

        else:
            try:
                create_convertors(response)
                response = dumps(response, cls=ConverterJSONEncoder)
            except CurrencyBaseException as exc:
                response = {exc.code: exc.message}
            except Exception as e:
                response = {'error': str(e)}

        source.last_run_result = response
        source.last_run_time = datetime.now()
        source.save()

        return response
