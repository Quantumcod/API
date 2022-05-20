import json
import os
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.auth import authenticate

from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad
from struct import pack
from rest_framework.test import APIClient
from applications.authentication.models import Roles,Permissions,PermissionsRoles,Users

class ClientInteractionTestCase (APITestCase):
    
    def setUp(self):
        
        client_wallet = ""
    
    def request_post(self, url_api, data__):
        json_data = json.dumps(data__)
        response = self.client.post(url_api,json_data, content_type='application/json')
        return response
        #print(json.loads(response.content))
    
    def test_clients_clients_list(self):
        print("---------------------------Clients----------------------------")
        
        print("clients_clients_list correct")
        response = self.client.get("/clients/clients/")
        self.assertEqual(response.status_code, 200)
    
    def test_clients_clients_create(self):
        print("clients_clients_create correct")
        response__ = {
            "pk": 1,
            "uuid": "self.gesssssssss",
            "Active": True
        }
        data = {
            "uuid": "self.gesssssssss",
            "Active": True
        }
        
        #self.assertEqual(json.loads(response.content), response__ )
        self.client_wallet = self.request_post("/clients/mobile/clients/", data)
        self.assertEqual(self.client_wallet.status_code, 201)
        
    
    
    def test_clients_mobile_relations_create(self):
        data__ = {
            "uuid"    : 1,
            "Address" : "TEztyZtB2eFB98YNaSHXo1dW6b7ChDK5gV"
        }
        userauth = authenticate(username='developer', password='9780bitcoin')
        print(userauth)
        print("clients_mobile_relations_create correct")
        response = self.request_post("/clients/mobile/relations/", data__)
        self.assertEqual(response.status_code, 201)
        #self.assertEqual(response.status_code, 200)  
        #self.assertEqual(response.status_code, 201)
"""
    def getUuid(self):
        bs = Blowfish.block_size
        data = b"secret aaaaaa aaaa aaaa aaaaa aaaa aaaa aaa kkfkkf ldldld ldldld ldldld"
        password = b'2AAFDD2ECE8B9F7D314E852E89C88'
        
        cipher = Blowfish.new(password, Blowfish.MODE_ECB)
        plen = bs - len(data) % bs
        padding = [plen]*plen
        padding = pack('b'*plen, *padding)
        msg = cipher.encrypt(data + padding)
    
        return msg
"""