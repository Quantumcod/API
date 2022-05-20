from rest_framework.routers import DefaultRouter
from .views import (
    CompanyWalletsViewSet
)
router = DefaultRouter()
router.register('companywallets',
                CompanyWalletsViewSet, basename='companywallets')
app_name = 'company'
urlpatterns = [

]
urlpatterns += router.urls