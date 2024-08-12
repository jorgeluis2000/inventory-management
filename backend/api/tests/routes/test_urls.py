from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.controllers.login import LoginViewSet
from api.controllers.product import ProductViewSet

class TestUrls(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_login_url_resolves(self):
        url = reverse('credentials-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, LoginViewSet)
    
    def test_product_url_resolves(self):
        url = reverse('products-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, ProductViewSet)