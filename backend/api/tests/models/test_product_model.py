from decimal import Decimal
from django.test import TestCase
from api.models.product import Product
from api.models.inventory import Inventory

class ProductModelTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            serial='ABC123',
            price=Decimal('29.99')
        )
    
    def test_increase_inventory_create(self):
        """
        Prueba que un inventario se cree correctamente cuando no existe para el producto.
        """
        self.product.increase_inventory(10)
        inventory = Inventory.objects.get(product_id=self.product)
        self.assertEqual(inventory.count, 10)

    def test_increase_inventory_update(self):
        """
        Prueba que la cantidad en el inventario se actualice correctamente si ya existe.
        """
        Inventory.objects.create(product_id=self.product, count=5)
        self.product.increase_inventory(10)
        inventory = Inventory.objects.get(product_id=self.product)
        self.assertEqual(inventory.count, 15)

    def test_increase_inventory_negative_amount(self):
        """
        Prueba que se lance una excepción si la cantidad es negativa.
        """
        with self.assertRaises(ValueError):
            self.product.increase_inventory(-5)

    def test_increase_inventory_zero_amount(self):
        """
        Prueba que se lance una excepción si la cantidad es cero.
        """
        with self.assertRaises(ValueError):
            self.product.increase_inventory(0)

    def test_product_creation(self):
        """Prueba que una instancia de Product se cree correctamente."""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.serial, 'ABC123')
        self.assertEqual(self.product.price, Decimal('29.99'))
        self.assertIsNotNone(self.product.created_at)
        self.assertIsNotNone(self.product.updated_at)

    def test_product_str_method(self):
        """Prueba el método __str__ del modelo Product."""
        self.assertEqual(str(self.product), f"{self.product.id} {self.product.name}")

    def test_update_product(self):
        """Prueba que se pueda actualizar un objeto Product."""
        self.product.name = 'Updated Product'
        self.product.price = Decimal('49.99')
        self.product.save()
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.name, 'Updated Product')
        self.assertEqual(updated_product.price, Decimal('49.99'))

    def test_delete_product(self):
        """Prueba que se pueda eliminar un objeto Product."""
        self.product.delete()
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=self.product.id)

    def test_unique_serial(self):
        """Prueba que el campo serial sea único."""
        product2 = Product(
            name='Another Product',
            serial='XYZ789',
            price=Decimal('15.99')
        )
        product2.save()
        with self.assertRaises(Exception):
            product3 = Product(
                name='Duplicate Product',
                serial='XYZ789',
                price=Decimal('100.00')
            )
            product3.save()
