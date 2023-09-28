from datetime import datetime, timedelta

import requests
import xmltodict
from celery import shared_task

from converter.models import Converter, User, Source
from converter.consts import METHODS


@shared_task
def get_currency():
    conv = Converter.objects.filter(id=1).first()
    if conv:
        method = METHODS.get(conv.autoload_method)
        sources = Source.objects.filter(is_active=True)
        if not sources:
            return 'No active sources'
        else:
            for source_obj in sources:
                response = requests.request('GET', source_obj.link)
                if response.status_code != 200:
                    return 'Invalid response'

                source_method = method
                if source_method:
                    source_method(source_obj, response)
                else:
                    return 'Invalid method'


@shared_task
def testing():
    return 'TESTING'
