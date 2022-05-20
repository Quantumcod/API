import logging
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from drf_yasg.utils import swagger_auto_schema
from .models import CompanyWallets
from .serializers import (
    CompanyWalletsSerializer, CompanyWalletsDetailSerializer)

logging.basicConfig(filename = settings.LOG_FILE, level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s: %(message)s')


class CompanyWalletsViewSet(ModelViewSet):
    """
    Description: View to display to company wallets (panel) 
    Author: Yessica Chuctaya 
    Date Created:  dd/mm/2021
    Date of last modification: 29/03/2022
    """
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    serializer_class = CompanyWalletsDetailSerializer
    queryset = CompanyWallets.objects.all()

    @swagger_auto_schema(
        responses={200: CompanyWalletsSerializer},
        request_body=CompanyWalletsSerializer)
    def create(self, request, *args, **kwargs):
        """
        Method to create a CompanyWallets
        """
        self.serializer_class = CompanyWalletsSerializer
        listwallet = CompanyWallets.objects.filter(
            Address=request.data['Address'],
            Cryptocurrency=request.data['Cryptocurrency'])

        if len(listwallet) > 0:
            return Response(data=False, status=HTTP_400_BAD_REQUEST)
        else:
            serializer = CompanyWalletsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=request.data, status=HTTP_201_CREATED)
