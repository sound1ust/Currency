from converter.models import Converter
from converter.serializers import CurrencyGetSerializer
from converter.utils import get_dict_key
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class CurrencyViewSet(viewsets.ModelViewSet):
    model = Converter
    serializer_class = CurrencyGetSerializer
    queryset = Converter.objects.all()

    def handle_response(self, request):

        handled_dict = {
            'output_ticker': request.query_params.get('output_ticker'),
            'input_ticker': request.query_params.get('input_ticker'),
            'source_date': request.query_params.get('source_date'),
            'source_id': request.query_params.get('source_id', '-1'),
        }

        return handled_dict

    @action(
        detail=False,
        methods=['get'],
    )
    def get_currency_rate(self, request):
        handled_dict = self.handle_response(request)
        if not all(handled_dict.values()):
            return Response(
                {'detail': 'Missing one or more required parameters.'},
                status=400,
            )

        key = get_dict_key(handled_dict)
        cached_currency_rate = cache.get(key)

        if not cached_currency_rate:
            currency = (
                Converter.objects.filter(
                    source_date__lte=handled_dict['source_date'],
                    output_ticker=handled_dict['output_ticker'],
                    input_ticker=handled_dict['input_ticker'],
                    source_id=handled_dict['source_id'],
                )
                .order_by(
                    '-source_date',
                    '-created_at',
                    '-id',
                )
                .first()
            )

            if currency:
                value = CurrencyGetSerializer(currency).data
                cache.set(key, value)
                return Response(
                    status=200,
                    data=value,
                )
        else:
            return Response(
                status=200,
                data={'rate': cached_currency_rate.get('rate')},
            )

        if not currency:
            return Response(
                status=204,
                data={'rate': None},
            )
