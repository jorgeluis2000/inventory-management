from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from api.usecase.product.serializers import ProductSerializer, ProductUpdateSerializer, Product, Inventory
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class ProductViewSetTest(TestCase):
    
    def setUp(self):
        """
        Se ejecuta antes de cada prueba.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.product = Product.objects.create(
            name='Test Product',
            serial='ABC123',
            price=100.00
        )
        
        self.inventory = Inventory.objects.create(
            product_id=self.product,
            count=10
        )
        
        self.url = f'/api/products/{self.product.id}/'
    
    def test_list_products(self):
        """
        Verifica que la lista de productos se retorne correctamente.
        """
        url = reverse('products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_create_product(self):
        """
        Verifica que un producto se cree correctamente.
        """
        url = reverse('products-list')
        
        data = {
            'name': 'New Product',
            'serial': 'XYZ789',
            'price': 200.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        
    def test_retrieve_product(self):
        """
        Verifica que un producto se recupere correctamente.
        """
        url = reverse('products-detail', args=[self.product.id])
        response = self.client.get(url)
        serializer = ProductSerializer(self.product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    def test_update_product(self):
        """
        Verifica que un producto se actualice correctamente.
        """
        data = {
            'name': 'Updated Product',
            'price': 150.00
        }
        url = reverse('products-detail', args=[self.product.id])
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(self.product.price, 150.00)
    
    def test_partial_update_product(self):
        """
        Verifica que el método PATCH no esté permitido.
        """
        data = {
            'name': 'Partially Updated Product'
        }
        url = reverse('products-detail', args=[self.product.id])
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_delete_product(self):
        """
        Verifica que un producto se elimine correctamente.
        """
        url = reverse('products-detail', args=[self.product.id])
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
    
    def test_increase_inventory_success(self):
        """
        Verifica que el inventario se aumente correctamente.
        """
        url = reverse('products-detail', args=[self.product.id])
        data = {'count': 5}
        response = self.client.post(f'{url}increase_inventory/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.count, 15)
    
    def test_increase_inventory_invalid_amount(self):
        """
        Verifica que se maneje un error si la cantidad de inventario no es válida.
        """
        url = reverse('products-detail', args=[self.product.id])
        data = {'count': -5}
        response = self.client.post(f'{url}increase_inventory/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Amount must be positive.')
    
    def test_create_product_duplicate_serial(self):
        """
        Verifica que se maneje un error si se intenta crear un producto con un número de serie duplicado.
        """
        url = reverse('products-list')
        Product.objects.create(
            name='Another Product',
            serial='DUPLICATE123',
            price=200.00
        )
        self.product.refresh_from_db()
        data = {
            'name': 'New Product',
            'serial': 'DUPLICATE123',
            'price': 150.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)