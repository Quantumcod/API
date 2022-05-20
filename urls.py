from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ClientsViewSet,
    ClientsListCreate,
    RelationsApiView
)
router = DefaultRouter()
router.register('clients',
                ClientsViewSet, basename='clients')

app_name = 'clients'

urlpatterns = [
    path('mobile/clients/',
         ClientsListCreate.as_view(), name='mobileClients'),
    path('mobile/relations/',
         RelationsApiView.as_view(), name='addressClientRelations'),
]
urlpatterns += router.urls
