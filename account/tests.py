# from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import User

# Create your tests here.
class CustomUserAPITestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('apiregister')
        self.login_url = reverse('apilogin')
        self.client = APIClient(enforce_csrf_checks=True)
        self.user_data = {
            'name': 'Apple',
            'email': 'a@a.com',
            'password': 'M4334890',
            'password2': 'M4334890',
            'tc': True
        }

        self.user = User.objects.create(
                name=self.user_data.get('name'),
                email=self.user_data.get('email'),
                password=make_password(self.user_data.get('password')),
                tc=self.user_data.get('tc')
            )
        
        self.token = Token.objects.create(user=self.user)

    def test_api_register(self):

        self.user_data = {
            'name': 'dple',
            'email': 'm@m.com',
            'password': 'M4334890',
            'password2': 'M4334890',
            'tc': True
        }

        response = self.client.post(self.register_url, data=self.user_data)
        # print("This is response", response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_login(self):
        # self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
        response = self.client.post(self.login_url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_user_profile(self):
        self.profile_url = reverse("apiprofile")
        self.client.force_authenticate(self.user)
        response = self.client.get(self.profile_url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_change_password(self):
        self.change_password = {
            'password': 'M4334891',
            'password2': 'M4334891',
        }

        self.user_data1 = {
            'name': 'Apple',
            'email': 'a@a.com',
            'password': 'M4334891',
            'password2': 'M4334891',
            'tc': True
        }

        self.change_password_url = reverse("apichangepassword")
        self.client.force_authenticate(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.change_password_url, data=self.change_password)
        # print("sadds", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        # self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
        response = self.client.post(self.login_url, data=self.user_data1)
        # print("game", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

