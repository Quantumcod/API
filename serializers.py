from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Roles, Users, Permissions, PermissionsRoles


class PermissionsRolesSerializer(serializers.ModelSerializer):
    """
    Class to serialize Permissions model
    """
    pk = serializers.IntegerField(source='Permission.pk')
    Name = serializers.CharField(source='Permission.Name')

    class Meta:
        model = PermissionsRoles
        fields = [
            'pk',
            'Name',
            'Read',
            'Update',
            'Delete',
            'Create',
            'Active'
        ]


class PermissionsSerializer(serializers.ModelSerializer):
    """
    Class to serialize Permissions model
    """
    class Meta:
        model = Permissions
        fields = [
            'pk',
            'Name',
            'Description',
            'Icon',
            'Url',
            'Active'
        ]


class RolesSerializer(serializers.ModelSerializer):
    """
    Class to serialize Roles model
    """
    class Meta:
        model = Roles
        fields = [
            'pk',
            'Name',
            'Description',
            'Permissions',
            'Active',
        ]


class RolesDetailSerializer(serializers.ModelSerializer):
    """
    Class to serialize Roles model
    """
    Permissions = PermissionsRolesSerializer(
        many=True, source='RolePermissionRoles')

    class Meta:
        model = Roles
        fields = [
            'pk',
            'Name',
            'Description',
            'Active',
            'Permissions'
        ]


class RolesUserSerializer(serializers.ModelSerializer):
    """
    Class to serialize Roles model
    """
    pk = serializers.IntegerField(source='id')
    Permissions = PermissionsSerializer(many=True)

    class Meta:
        model = Roles
        fields = [
            'pk',
            'Name',
            'Permissions'
        ]


class UsersSerializer(serializers.ModelSerializer):
    """
    Class to serialize Users model
    """
    Username = serializers.CharField(required=False, source='username')
    Name = serializers.CharField(required=False, source='first_name')
    LastName = serializers.CharField(required=False, source='last_name')
    Email = serializers.CharField(required=False, source='email')
    Roles = RolesUserSerializer(many=True)

    class Meta:
        model = Users
        fields = [
            'pk',
            'Username',
            'Email',
            'Name',
            'LastName',
            'Roles'
        ]


class UsersDetailSerializer(serializers.ModelSerializer):
    """
    Class to serialize Users model
    """
    Username = serializers.CharField(required=False, source='username')
    Name = serializers.CharField(required=False, source='first_name')
    LastName = serializers.CharField(required=False, source='last_name')
    Email = serializers.CharField(required=False, source='email')
    Roles = RolesDetailSerializer(many=True)

    class Meta:
        model = Users
        fields = [
            'pk',
            'Username',
            'Email',
            'Name',
            'LastName',
            'Roles'
        ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Class to serialize Tokens model 
    """

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        # Add extra responses here
        try:
            data['user'] = UsersDetailSerializer(
                Users.objects.get(pk=self.user.pk)).data
        except Exception as e:
            data['user'] = UserSerializer(self.user).data
            data['user']['Roles'] = []
        return data

    @classmethod
    def get_token(cls, user):
        tok = super().get_token(user)
        return tok


class UserSerializer(serializers.ModelSerializer):
    """
    Class to serialize Users model
    """
    Username = serializers.CharField(required=False, source='username')
    Name = serializers.CharField(required=False, source='first_name')
    LastName = serializers.CharField(required=False, source='last_name')
    Email = serializers.CharField(required=False, source='email')

    class Meta:
        model = User
        fields = [
            'pk',
            'Username',
            'Email',
            'Name',
            'LastName',
        ]


class RefreshTokenSerializer(serializers.Serializer):
    access = serializers.CharField()
