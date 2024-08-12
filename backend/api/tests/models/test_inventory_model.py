from django.test import TestCase
from api.models.product import Product
from api.models.inventory import Inventory

class InventoryModelTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name='Test Product', price=10.00)
        self.inventory = Inventory.objects.create(product_id=self.product, count=100)

    def test_inventory_creation(self):
        """Prueba que una instancia de Inventory se cree correctamente."""
        self.assertEqual(self.inventory.product_id, self.product)
        self.assertEqual(self.inventory.count, 100)

    def test_inventory_str_method(self):
        """Prueba el método __str__ del modelo Inventory."""
        self.assertEqual(str(self.inventory), f"{self.inventory.id} - ({self.inventory.product_id}) - {self.inventory.count}")

    def test_update_inventory(self):
        """Prueba que se pueda actualizar un objeto Inventory."""
        self.inventory.count = 150
        self.inventory.save()
        updated_inventory = Inventory.objects.get(id=self.inventory.id)
        self.assertEqual(updated_inventory.count, 150)

    def test_delete_inventory(self):
        """Prueba que se pueda eliminar un objeto Inventory."""
        self.inventory.delete()
        with self.assertRaises(Inventory.DoesNotExist):
            Inventory.objects.get(id=self.inventory.id)

    def test_inventory_count_default(self):
        """Prueba que el campo count tenga el valor por defecto."""
        inventory = Inventory.objects.create(product_id=self.product)
        self.assertEqual(inventory.count, 0)
