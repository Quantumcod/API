import logging
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import get_connection, EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.shortcuts import render
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenRefreshSerializer)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_401_UNAUTHORIZED,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_204_NO_CONTENT)
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Permissions, PermissionsRoles, Roles, Users
from .serializers import (
    MyTokenObtainPairSerializer, RefreshTokenSerializer,
    UsersSerializer, PermissionsSerializer,
    RolesSerializer, RolesDetailSerializer)
logging.basicConfig(filename=settings.LOG_FILE, level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s: %(message)s')


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_id='Returns a JSON Web Token (JWT)' +
        'that can be used for authenticated requests',
        operation_description='API View that receives a POST with a user' +
        's username and password',
        responses={"200": TokenRefreshSerializer, "400": 'Bad Request'}))
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(
            username=username,
            password=password
        )
        if user:
            requestSerializer = self.serializer_class(data=request.data)
            if requestSerializer.is_valid():
                dataResponse = requestSerializer.validated_data
                if User.objects.get(pk=dataResponse['user']['pk']).is_staff:
                    return Response(data=dataResponse, status=HTTP_200_OK)
                return Response(data={'unauthorized user'},
                                status=HTTP_401_UNAUTHORIZED)
        else:
            return Response(
                data={'Users not exist.'},
                status=HTTP_400_BAD_REQUEST)


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_id='Returns a refresh JSON Web Token (JWT)' +
        'that can be used for authenticated requests',
        operation_description='API View that receive a refresh token',
        responses={"200": RefreshTokenSerializer, "400": 'Bad Request'}))
class MyRefreshTokenObtainPairView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


class UserViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated]
    serializer_class = UsersSerializer
    queryset = Users.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: UsersSerializer})
    def create(self, request, *args, **kwargs):
        """
        Method to create a user with their respective roles
        """
        data = request.data
        # Create User
        user = Users.objects.create(
            first_name=data['Name'],
            last_name=data['LastName'],
            username=data['Username'],
            email=data['Email'],
            is_staff=True,
        )
        # Set password by default '9780wallet'
        user.set_password('9780wallet')
        # Set rol
        for rol in data['Roles']:
            user.Roles.add(rol['pk'])
        user.save()

        # send Email by change pasword
        try:
            sendEmail(user, request, 'Set up here your password')
        except Exception as e:
            logging.error('UserViewSet : ' +
                          'Not send email by change password' + str(e))

        return Response(
            data=UsersSerializer(instance=user).data,
            status=HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Method to update a user with their respective roles
        """
        data = request.data
        user = Users.objects.get(pk=self.kwargs.get('pk'))
        user.first_name = data['Name']
        user.last_name = data['LastName']
        user.username = data['Username']
        user.email = data['Email']
        user.Roles.clear()
        for rol in data['Roles']:
            user.Roles.add(rol['pk'])
        user.save()
        return Response(
            data=UsersSerializer(instance=user).data,
            status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Method delete that change is_active user status to false
        """
        user = Users.objects.get(pk=self.kwargs.get('pk'))
        user.is_active = False
        user.save()
        return Response(data=None, status=HTTP_204_NO_CONTENT)


class PermissionViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'delete']
    serializer_class = PermissionsSerializer
    queryset = Permissions.objects.filter(Active=True, Deleted=False)

    def destroy(self, request, *args, **kwargs):
        """
        Method delete that change Active permission status to false
        """
        permission = Permissions.objects.get(pk=self.kwargs.get('pk'))
        permission.Deleted = False
        permission.save()
        return Response(data=None, status=HTTP_204_NO_CONTENT)


class RolesViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = RolesSerializer
    queryset = Roles.objects.filter(Active=True, Deleted=False)

    @swagger_auto_schema(responses={200: RolesDetailSerializer},
                         request_body=RolesDetailSerializer)
    def create(self, request, *args, **kwargs):
        """
        Method to create a roles with their respective permissions
        """
        permissions = self.request.data.pop('Permissions')
        rol = Roles.objects.create(**request.data)
        for permission in permissions:
            rol.Permissions.add(
                Permissions.objects.get(pk=permission['pk']),
                through_defaults={
                    'Read': permission['Read'],
                    'Update': permission['Update'],
                    'Delete': permission['Delete'],
                    'Create': permission['Create'],
                })
        return Response(data=RolesDetailSerializer(instance=rol).data,
                        status=HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: RolesDetailSerializer})
    def retrieve(self, request, pk):
        """
        Method to get detail from a roles and their respective permissions
        """
        roles = Roles.objects.filter(Active=True)
        rol = get_object_or_404(roles, pk=pk)
        serializer = RolesDetailSerializer(rol)
        return Response(data=serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(responses={200: RolesDetailSerializer},
                         request_body=RolesDetailSerializer)
    def update(self, request, *args, **kwargs):
        """
        Method to update a roles and their respective permissions
        """
        data = request.data
        permissions = data.pop('Permissions')
        rol = Roles.objects.get(pk=self.kwargs.get('pk'))
        rol.Name = data['Name']
        rol.Description = data['Description']
        rol.Active = data['Active']
        rol.save()
        rol.Permissions.clear()
        for permission in permissions:
            rol.Permissions.add(
                Permissions.objects.get(pk=permission['pk']),
                through_defaults={
                    'Read': permission['Read'],
                    'Update': permission['Update'],
                    'Delete': permission['Delete'],
                    'Create': permission['Create'],
                })
        return Response(data=RolesDetailSerializer(instance=rol).data,
                        status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        rol = Roles.objects.get(pk=self.kwargs.get('pk'))
        rol.Deleted = False
        rol.save()
        return Response(data=None, status=HTTP_204_NO_CONTENT)


def sendEmail(user, request, message):
    """
    Method to send email
    """
    token = PasswordResetTokenGenerator().make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    email_template = render_to_string('email.html', context={
        'username': user.username,
        'protocol': request.scheme,
        'domain': request.META['HTTP_HOST'],
        'uidb64': uidb64,
        'message': message,
        'token': token
    })

    msg = EmailMultiAlternatives(
        'ADMINISTRACIÓN WALLET - CREDENCIALES',  # subject
        email_template,  # message =
        settings.EMAIL_HOST_USER,  # from_email =
        [user.email]  # [recipient] =
    )
    msg.attach_alternative(email_template, "text/html")
    msg.content_subtype = "html"
    msg.send(fail_silently=False)
    get_connection().send_messages(msg)


def restablecerExitoso(request):
    """
    Method that returns an html page after setting the password
    """
    try:
        x = urlopen(request.scheme + '://' + request.META['HTTP_HOST'])
        return HttpResponse(x.read())
    except:
        return render(request, "reset_complete.html")
