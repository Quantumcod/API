from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView
from rest_framework.routers import DefaultRouter
from .forms import EstablecerContrasena
from .views import (
    MyTokenObtainPairView,
    MyRefreshTokenObtainPairView,
    UserViewSet,
    PermissionViewSet,
    RolesViewSet,
    restablecerExitoso
)


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('permissions', PermissionViewSet, basename='permissions')
router.register('roles', RolesViewSet, basename='roles')
app_name = 'authentication'
urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token'),
    path('tokenRefresh/', MyRefreshTokenObtainPairView.as_view(),
         name='tokenRefresh'),
    path('password_reset/complete/', restablecerExitoso,
         name='password_reset_complete'),
    path('password_reset_confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='reset_password.html',
             form_class=EstablecerContrasena,
             success_url=reverse_lazy('authentication:password_reset_complete')
         ),
         name='password_reset_confirm'
         )

]
urlpatterns += router.urls
