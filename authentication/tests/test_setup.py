import imp
from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetup(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url =reverse('login')

        self.user_data = {
            'email': 'g@gmail.com',
            'username': 'gboy',
            'password': 'gboy..12'
        }
        return super().setUp()
    

def tearDown(self):
    return super().tearDown()