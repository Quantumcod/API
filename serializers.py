from rest_framework import serializers
from .models import CompanyWallets


class CompanyWalletsDetailSerializer(serializers.ModelSerializer):
    """
    Class to serialize CompanyWallets Details model
    """
    CryptocurrencyName = serializers.CharField(
        source='Cryptocurrency.Name')

    class Meta:
        model = CompanyWallets
        fields = [
            'pk',
            'Address',
            'CryptocurrencyName',
            'Quantity',
            'Active'
        ]


class CompanyWalletsSerializer(serializers.ModelSerializer):
    """
    Class to serialize CompanyWallets model
    """
    class Meta:
        model = CompanyWallets
        fields = [
            'pk',
            'Address',
            'Cryptocurrency',
            'Active'
        ]