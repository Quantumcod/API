
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CryptocurrenciesViewSet,
    FeesAPIView,
    CommissionsExchangeAPIView,
    CryptocurrenciesAllListAPIView,
    CryptocurrenciesListAPIView,
    FeeByCryptocurrencyAPIView,
    FeeByToExchangesAPIView,
    FeeExFeeExchangesPkAPIView
)
router = DefaultRouter()
router.register('cryptocurrencies',
                CryptocurrenciesViewSet, basename='cryptocurrencies')
router.register('fees',
                FeesAPIView, basename='mobile_fees')
router.register('commissionsExchange',
                CommissionsExchangeAPIView, basename='commissionExchange')
app_name = 'cryptocurrencies'

urlpatterns = [
    path('mobile/cryptocurrencies/',
         CryptocurrenciesAllListAPIView.as_view(),
         name='mobile_cryptocurrencies'),
    path('mobile/cryptocurrencies/<str:pk>',
         CryptocurrenciesListAPIView.as_view(),
         name='mobile_pk_cryptocurrencies'),
    path('mobile/fees/<str:symbol>',
         FeeByCryptocurrencyAPIView.as_view(),
         name='mobile_fees'),
    path('mobile/exchanges/fees/<str:symbolFrom>/<str:symbolTo>/',
         FeeByToExchangesAPIView.as_view(),
         name='mobile_fees_exchange'),
    path('exchanges/fees/<str:pk>/',
         FeeExFeeExchangesPkAPIView.as_view(),
         name='fees_exchange_pk'),
]
urlpatterns += router.urls
