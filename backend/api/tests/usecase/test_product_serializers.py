from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict
from api.usecase.product.serializers import ProductSerializer, ProductUpdateSerializer, ProductFilter, Product, Inventory

class ProductSerializerTest(TestCase):
    
    def setUp(self):
        """
        Se ejecuta antes de cada prueba.
        """
        self.product = Product.objects.create(
            name='Test Product',
            serial='ABC123',
            price=100.00
        )
        self.inventory = Inventory.objects.create(
            product_id=self.product,
            count=10
        )
    
    def test_product_serializer_with_inventory(self):
        """
        Verifica que el campo 'count' en ProductSerializer sea correcto.
        """
        serializer = ProductSerializer(self.product)
        data = serializer.data
        self.assertEqual(data['count'], 10)

    def test_product_serializer_without_inventory(self):
        """
        Verifica que el campo 'count' en ProductSerializer sea 0 cuando no hay inventario.
        """
        self.inventory.delete()  # Elimina el inventario asociado
        serializer = ProductSerializer(self.product)
        data = serializer.data
        self.assertEqual(data['count'], 0)

class ProductUpdateSerializerTest(TestCase):
    
    def setUp(self):
        """
        Se ejecuta antes de cada prueba.
        """
        self.product = Product.objects.create(
            name='Test Product',
            serial='ABC123',
            price=100.00
        )

    def test_product_update_serializer_valid_data(self):
        """
        Verifica que el ProductUpdateSerializer maneje correctamente los datos válidos.
        """
        data = {
            'name': 'Updated Product',
            'serial': 'DEF456',
            'price': 150.00
        }
        serializer = ProductUpdateSerializer(instance=self.product, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_product = serializer.save()
        self.assertEqual(updated_product.name, 'Updated Product')
        self.assertEqual(updated_product.serial, 'DEF456')
        self.assertEqual(updated_product.price, 150.00)

    def test_product_update_serializer_duplicate_serial(self):
        """
        Verifica que ProductUpdateSerializer lance una excepción si se usa un serial duplicado.
        """
        Product.objects.create(
            name='Another Product',
            serial='XYZ789',
            price=200.00
        )
        data = {
            'serial': 'XYZ789'
        }
        serializer = ProductUpdateSerializer(instance=self.product, data=data, partial=True)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

class ProductFilterTest(TestCase):
    
    def setUp(self):
        """
        Se ejecuta antes de cada prueba.
        """
        self.product1 = Product.objects.create(
            name='Product One',
            serial='ONE123',
            price=50.00
        )
        self.product2 = Product.objects.create(
            name='Product Two',
            serial='TWO123',
            price=75.00
        )
    
    def test_filter_by_name(self):
        """
        Verifica que el filtro por nombre funcione correctamente.
        """
        filter_backend = ProductFilter(data={'name': 'One'})
        filtered_qs = filter_backend.qs
        self.assertIn(self.product1, filtered_qs)
        self.assertNotIn(self.product2, filtered_qs)

    def test_filter_by_serial(self):
        """
        Verifica que el filtro por serial funcione correctamente.
        """
        filter_backend = ProductFilter(data={'serial': 'TWO'})
        filtered_qs = filter_backend.qs
        self.assertIn(self.product2, filtered_qs)
        self.assertNotIn(self.product1, filtered_qs)

class ProductPaginationTest(TestCase):
    
    def setUp(self):
        """
        Se ejecuta antes de cada prueba.
        """
        for i in range(15):
            Product.objects.create(
                name=f'Product {i}',
                serial=f'SERIAL{i}',
                price=100.00
            )

    def test_pagination(self):
        """
        Verifica que la paginación funcione correctamente.
        """
        url = '/api/products/?page=1&page_size=10'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['count'], 15)

        url = '/api/products/?page=2&page_size=10'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['count'], 15)
