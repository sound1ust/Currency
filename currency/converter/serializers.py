from converter.models import Converter
from rest_framework import serializers


class CurrencyGetSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Converter
        fields = [
            'rate',
        ]

    @staticmethod
    def get_rate(obj):
        value = obj.value
        coefficient = obj.coefficient

        if value and coefficient:
            rate = value * coefficient
        else:
            rate = None

        return rate
