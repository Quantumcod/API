from rest_framework import serializers
from .models import Cryptocurrencies, Fees, Commission
from decimal import Decimal


class CryptocurrenciesListSerializer(serializers.ModelSerializer):
    """
    Class to serialize list of  Cryptocurrency model
    """
    class Meta:
        model = Cryptocurrencies
        fields = [
            'pk',
            'Symbol',
            'Name',
            'MinerFeeAverage',
            'MinerFee',
            'TotalFee',
            'Security',
            'ModifiableMinerfee',
            'Price',
            'Active'
        ]


class CryptocurrenciesUpdateSerializer(serializers.ModelSerializer):
    """
    Class to serialize update Cryptocurrency model
    """
    class Meta:
        model = Cryptocurrencies
        fields = [
            'Symbol',
            'MinerFee',
            'Security',
            'TotalFee',
            'Active',
        ]


class FeesSerializer(serializers.ModelSerializer):
    """
    Class to serialize CRUD Fees model
    """

    class Meta:
        model = Fees
        fields = [
            'pk',
            'Type',
            'AverageMinerFee',
            'Security',
            'Created',
            'Active',
            'Deleted'
        ]


class CommissionCreateSerializer(serializers.ModelSerializer):
    """
    Class to serialize commission of exchange 
    """
    class Meta:
        model = Commission
        exclude = ['Created', 'Update']

    def create(self, validated_data):
        commission = Commission.objects.create(**validated_data)
        return commission


class CryptocurrenciesSerializer(serializers.ModelSerializer):
    """
    Class to serialize Cryptocurrency model
    """

    class Meta:
        model = Cryptocurrencies
        fields = [
            'pk',
            'Symbol',
            'Name',
            'Logo',
            'Priority',
            'Active'
        ]


class FeeByCryptoSerializer(serializers.ModelSerializer):
    """
     Class to serialize fee for transactions by symbol
    """
    MinerFee = serializers.SerializerMethodField('get_MinerFee')

    class Meta:
        model = Cryptocurrencies
        fields = [
            'MinerFee',
            'Security',
            'TotalFee',
            'Min'
        ]

    def get_MinerFee(self, cryptocurrency):
        Symbols = ['ETH', 'SOL', 'TRX', 'USDTETH', 'SYS', 'AVAX']
        if cryptocurrency.Symbol in Symbols:
            MinerFee = Decimal(cryptocurrency.MinerFee) + \
                Decimal(cryptocurrency.MinerFee)
        else:
            MinerFee = cryptocurrency.MinerFee
        return MinerFee


class CommissionSerializer(serializers.ModelSerializer):
    """
    Class to serialize Commission model
    """
    class Meta:
        model = Commission
        fields = [
            'pk',
            'Min',
            'Max',
            'Percentage',
            'Fixed',
            'Variable',
        ]


class CryptocurrenciesFeesExchangeSerializer(serializers.ModelSerializer):
    """
    Class to serialize Cryptocurrency with commission for exchange by symbols
    """
    ComissionByCryptocurrency = CommissionSerializer(many=True)

    class Meta:
        model = Cryptocurrencies
        fields = [
            'pk',
            'Symbol',
            'Name',
            'MinerFee',
            'Security',
            'Price',
            'ComissionByCryptocurrency'
        ]
