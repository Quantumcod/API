from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework.permissions import IsAuthenticated, AllowAny

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


# Schema to describe documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Wallet API",
        default_version='v1',
        description="It is a wallet API created to" +
        " get, post, update data related to project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="9780desarrollador05@gmail.com"),
        license=openapi.License(name="9780 Capital"),
    ),
    public=True,
    permission_classes=[AllowAny]
)

# Urls to access views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('jet/', include('jet.urls', 'jet')),
    path('authentication/', include('applications.authentication.urls')),
    path('general/', include('applications.general.urls')),
    path('clients/', include('applications.clients.urls')),
    path('company/', include('applications.company.urls')),
    path('updates/', include('applications.updates.urls')),
    path('reports/', include('applications.reports.urls')),
    path('cryptocurrencies/', include('applications.cryptocurrencies.urls')),
    path('transactions/', include('applications.transactions.urls')),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
