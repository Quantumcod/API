from rest_framework import serializers
from .models import Clients, Addresses


class ClientsSerializer(serializers.ModelSerializer):
    """
    Class to serialize Clients model
    """
    class Meta:
        model = Clients
        fields = [
            'pk',
            'uuid',
            'Active'
        ]


class AddressesSerializer(serializers.ModelSerializer):
    """
    Class to serialize Addresses model
    """
    class Meta:
        model = Addresses
        fields = [
            'uuid',
            'Address'
        ]
