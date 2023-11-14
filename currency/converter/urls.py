from converter.viewsets import CurrencyViewSet
from django.urls import include
from django.urls import path
from rest_framework import routers

app_name = 'converter'

router = routers.DefaultRouter()
router.register(r'converter', CurrencyViewSet, basename='Currencies')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
