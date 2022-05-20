import json
import os
from django.urls import reverse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from applications.authentication.models import Roles,Permissions,PermissionsRoles,Users
#from django.contrib.auth.admin import 

class AuthTestCase (APITestCase):
    def setUp(self):
        print("---------------------------Token Generate----------------------------")
        permmiss = Permissions(
            Name="Rol",
            Description="Roles",
            Icon="aaaaaaaaa",
            Url="/rol",
            Created="2021-08-12T16:52:23.846Z",
            Active=True,
            Deleted= False
        )
        permmiss.save()
        
        rol = Roles(
            Name="Administrador",
            Description="Administrador",
            Created="2021-11-19T15:35:41.080Z",
            Active=True,
            Deleted=False
        )
        rol.save()
        
        permiss_roles = PermissionsRoles(
            Permission_id=1,
            Role_id=1,
            Read=True,
            Update=True,
            Delete=True,
            Create=True,
            Created="2021-11-19T15:35:41.080Z",
            Active=True,
            Deleted=False
        )
        permiss_roles.save()
        
        user = User(
            first_name = "developer",
            last_name = "developer",
            username = "developer",
            email = "aaa@gmail.com"
        )
        user.set_password("9780bitcoin")
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        
        user_auth = Users(
            Created="2021-11-19T15:35:41.080Z"
        )
        user_auth.save()
        user_auth.Roles.set([1])
        user_auth.save()
        
        # permmiss_list = Permissions.objects.all()
        # rol_list = Roles.objects.all()
        # permiss_roles_list = PermissionsRoles.objects.all()
        # user_ser_list = Users.objects.all()
        userauth = authenticate(username='developer', password='9780bitcoin')
        # print(permmiss_list.values())
        # print(rol_list.values())
        # print(permiss_roles_list.values())
        # print(user_ser_list.values())
        print(userauth)
        
    
    def test_createToken(self):    
        print("authentication_token")
        authentification = {
            "username": "developer",
            "password": "9780bitcoin"
        }
        
        json_data = json.dumps(authentification)
        response = self.client.post(
            "/authentication/token/", json_data, content_type='application/json')
        response_ = json.loads(response.content)

        print(response_['access'])
        #self.auth_token = response.content.access
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.status_code, 201)
        os.environ['TOKEN'] = response_['access']