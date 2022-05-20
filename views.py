import logging
from decimal import Decimal
from django.conf import settings
from django.db.models import Q
from django.db.models import Case, When, IntegerField
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Prefetch
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from drf_yasg.utils import swagger_auto_schema
from ..authentication.permissions import (
    permissionRoles, Create, Update, Delete, Get)
from .models import Commission, Cryptocurrencies, Fees
from .serializers import (
    CryptocurrenciesListSerializer, CryptocurrenciesUpdateSerializer,
    FeesSerializer, CommissionCreateSerializer, CryptocurrenciesSerializer,
    FeeByCryptoSerializer, CryptocurrenciesFeesExchangeSerializer)

logging.basicConfig(filename=settings.LOG_FILE, level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s: %(message)s')


class CryptocurrenciesViewSet(ModelViewSet):
    """ 
    Description: View to get, put  cryptocurrencies (panel)
    Author: Suling Vera 
    Date Created: dd/mm/2021
    Date of last modification: 31/03/2022
    """
    http_method_names = ['get', 'put', 'delete']
    serializer_class = CryptocurrenciesListSerializer
    permission_classes = {
        IsAuthenticated: False,
        Get: True,
        Create: False
    }
    queryset = Cryptocurrencies.objects.all()

    def get_permissions(self):
        self.permission_classes = permissionRoles(
            self.request, '/usuarios', self.permission_classes)
        return super(CryptocurrenciesViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return CryptocurrenciesListSerializer
        elif self.action == 'update':
            return CryptocurrenciesUpdateSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def put(self, request, pk=None):
        data_request = request.data

        cryptocurrency = Cryptocurrencies.objects.get(pk=pk)
        cryptocurrency.Symbol = data_request['Symbol']
        cryptocurrency.Security = Decimal(f"{(data_request['Security']):.8f}")
        cryptocurrency.TotalFee = Decimal(f"{(data_request['TotalFee']):.8f}")
        cryptocurrency.Active = data_request['Active']
        cryptocurrency.save(update_fields=[
            'MinerFee', 'Security', 'TotalFee', 'Active'])

        CryptocurrenciesUpdate = CryptocurrenciesUpdateSerializer(
            instance=Cryptocurrencies.objects.get(pk=pk))

        return Response(
            data=CryptocurrenciesUpdate.data, status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Method delete that change Deleted Cryptocurrencies status to True
        """
        cryptocurrency = Cryptocurrencies.objects.get(
            pk=self.kwargs.get('pk'))
        cryptocurrency.Deleted = True
        cryptocurrency.save()
        return Response(data=None, status=HTTP_204_NO_CONTENT)


class FeesAPIView(ModelViewSet):
    """ 
    Description: View to CRUD of Fee in  transactions by symbol 
                 cryptocurrencies (panel) 
    Author: Suling Vera 
    Date Created: dd/mm/2021
    Date of last modification: 31/03/2022
    """
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'post', 'delete']
    serializer_class = FeesSerializer
    queryset = Fees.objects.all()

    def destroy(self, request, *args, **kwargs):
        """
        Method delete that change Deleted Cryptocurrencies status to True
        """
        Fee = Fees.objects.get(pk=self.kwargs.get('pk'))
        Fee.Deleted = True
        Fee.save()
        return Response(data={}, status=HTTP_204_NO_CONTENT)


class CommissionsExchangeAPIView(ModelViewSet):
    """ 
    Description: View to put and post of commission of exchange by symbol 
                cryptocurrencies (panel)
    Author: Suling Vera 
    Date Created: dd/mm/2021
    Date of last modification: 31/03/2022
    """
    permission_classes = [AllowAny]  # IsAuthenticated
    http_method_names = ['put', 'post']
    serializer_class = CommissionCreateSerializer
    queryset = Commission.objects.all()

    permission_classes = {
        IsAuthenticated: False,
        Get: True,
        Create: False
    }

    def put(self, request, pk=None):
        commission = Commission.objects.filter(pk=pk)
        commission.update(**request.data)
        commission.save()

        return Response(
            data=CommissionCreateSerializer(instance=commission).data,
            status=HTTP_200_OK)


class CryptocurrenciesAllListAPIView(ListAPIView):
    """ 
    Description: View to list all cryptocurrencies 
                 cryptocurrencies (mobil)
    Author: Suling Vera 
    Date Created: dd/mm/2021
    Date of last modification: 31/03/2022
    """
    permission_classes = [AllowAny]
    http_method_names = ['get', ]
    serializer_class = CryptocurrenciesSerializer
    queryset = Cryptocurrencies.objects.all().annotate(
        priority=Case(When(Priority='HIGH', then=1),
                      When(Priority='MEDIUM', then=2),
                      When(Priority='LOW', then=3),
                      output_field=IntegerField())
    ).order_by('priority')


class CryptocurrenciesListAPIView(ListAPIView):
    """ 
    Description: View to list cryptocurrencies by pk 
                 cryptocurrencies (mobil)
    Author: Suling Vera 
    Date Created: dd/mm/2021
    Date of last modification: 31/03/2022
    """
    permission_classes = [AllowAny]
    http_method_names = ['get']
    serializer_class = CryptocurrenciesSerializer

    @swagger_auto_schema(
        responses={"200": CryptocurrenciesSerializer, "400": 'Bad Request'})
    def get_queryset(self):
        if self.kwargs.get('pk'):
            return Cryptocurrencies.objects.filter(pk=self.kwargs.get('pk'))
        else:
            return None


class FeeByCryptocurrencyAPIView(ListAPIView):
    """ 
    Description: View to fee for transactions by symbol
                 cryptocurrencies (mobil)
    Author: Suling Vera 
    Date Created: dd/mm/2021
    Date of last modification: 31/03/2022
    """
    permission_classes = [AllowAny]
    http_method_names = ['get']
    serializer_class = FeeByCryptoSerializer

    @swagger_auto_schema(
        responses={"200": FeeByCryptoSerializer, "400": 'Bad Request'})
    def get_queryset(self):
        getSymbol = self.kwargs.get('symbol').upper()
        if self.kwargs.get('symbol'):
            return Cryptocurrencies.objects.filter(
                Symbol=getSymbol)
        else:
            return None


class FeeByToExchangesAPIView(ListAPIView):
    """ 
    Description: View to fee for exchange by symbols
                 cryptocurrencies (mobil)
    Author: Suling Vera 
    Date Created: dd/mm/2021
    Date of last modification: 31/03/2022
    """
    permission_classes = [AllowAny]
    http_method_names = ['get']
    serializer_class = CryptocurrenciesFeesExchangeSerializer

    @swagger_auto_schema(
        responses={"200": CryptocurrenciesFeesExchangeSerializer,
                   "400": 'Bad Request'})
    def get_queryset(self):
        symbolFrom = self.kwargs.get('symbolFrom').upper()
        symbolTo = self.kwargs.get('symbolTo').upper()

        # Queryset : will first search for 2 cryptocurrencie,
        # pfor each cryptocurrency, it will filter out the commissions
        # that are active and the Deleted field is set to false Prefetch
        # Filter Nested serializer Django Rest Framework
        cryptocurrencies = Cryptocurrencies.objects.filter(
            (Q(Symbol=symbolFrom) | Q(Symbol=symbolTo)) & Q(Active=True))\
            .prefetch_related(
            Prefetch('ComissionByCryptocurrency',
                     queryset=Commission.objects.filter(
                         Active=True,
                         Deleted=False)
                     )
        )

        return cryptocurrencies


class FeeExFeeExchangesPkAPIView(ListAPIView):
    """ 
    Description: View to fee for exchange by pk
                 cryptocurrencies 
    Author: Suling Vera 
    Date Created: dd/mm/2021
    Date of last modification: 31/03/2022
    """
    permission_classes = [IsAuthenticated]  # IsAuthenticated
    http_method_names = ['get']
    serializer_class = CryptocurrenciesFeesExchangeSerializer

    @swagger_auto_schema(
        responses={"200": CryptocurrenciesFeesExchangeSerializer,
                   "400": 'Bad Request'})
    def get_queryset(self):
        if self.kwargs.get('pk'):
            cryptocurrency = Cryptocurrencies.objects.filter(
                pk=self.kwargs.get('pk'), Active=True)
            return cryptocurrency
        else:
            return None
