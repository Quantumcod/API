import logging
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)
from .models import Clients, Addresses
from .serializers import ClientsSerializer, AddressesSerializer
from drf_yasg.utils import swagger_auto_schema

logging.basicConfig(filename = settings.LOG_FILE, level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s: %(message)s')


class ClientsViewSet(ModelViewSet):
    """
    Description: View to display get and create Clients
    Author: Suling Vera 
    Date Created:  dd/mm/2021
    Date of last modification: 28/03/2022
    """
    queryset = Clients.objects.all()
    http_method_names = ['get', 'post']
    permission_classes = [AllowAny]
    serializer_class = ClientsSerializer


class ClientsListCreate(ListCreateAPIView):
    """
    Description: View to display list and create Clients by mobile
    Author: Yessica Chuctaya 
    Date Created:  dd/mm/2021
    Date of last modification: 28/03/2022
    """
    http_method_names = ['get', 'post']
    serializer_class = ClientsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        In case of list Clients in mobile 
        """
        if self.kwargs.get('uuid'):
            return Clients.objects.filter(uuid=self.kwargs.get('uuid'))
        else:
            return None

    def create(self, request, *args, **kwargs):
        """
        In case of create Clients in mobile 
        """
        serializer = ClientsSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        except Exception as e:
            data = serializer.data
            client = Clients.objects.get(uuid=data['uuid'])
            return Response(
                data=ClientsSerializer(client).data, status=HTTP_201_CREATED)


class RelationsApiView(APIView):

    """
    Description: View to display create relations between Clients and address
                by mobile
    Author: Yessica Chuctaya
    Date Created:  11/09/2021
    Modification date: 28/03/2022

    """
    http_method_names = ['post']
    permission_classes = [AllowAny]
    serializer_class = AddressesSerializer

    @swagger_auto_schema(request_body=AddressesSerializer,
                         responses={"200": AddressesSerializer,
                                    "400": 'Bad Request'})
    def post(self, request):
        data = request.data
        response = {
            'status': '',
            'message': ''
        }

        try:
            client = Clients.objects.get(pk=data['uuid'])

        except Exception as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return Response(data=response, status=HTTP_400_BAD_REQUEST)
        try:
            address = Addresses.objects.get(uuid=client,
                                            Address=data['Address'])
        except Exception as e:
            address = Addresses.objects.create(
                uuid=client,
                Address=data['Address']
            )
        return Response(
            data=AddressesSerializer(address).data, status=HTTP_200_OK)
