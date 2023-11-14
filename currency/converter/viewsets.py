from converter.models import Converter
from converter.serializers import CurrencyGetSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class CurrencyViewSet(viewsets.ModelViewSet):
    model = Converter
    serializer_class = CurrencyGetSerializer
    queryset = Converter.objects.all()

    def handle_response(self, request):
        output_ticker = request.query_params.get('output_ticker')
        input_ticker = request.query_params.get('input_ticker')
        source_date = request.query_params.get('source_date')
        source_id = request.query_params.get('source_id')

        if not source_id:
            source_id = '1'

        handled_dict = {
            'output_ticker': output_ticker,
            'input_ticker': input_ticker,
            'source_date': source_date,
            'source_id': source_id,
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

        if not currency:
            return Response({'rate': None})
        else:
            return Response(CurrencyGetSerializer(currency).data)
