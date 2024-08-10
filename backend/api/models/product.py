from django.db import models 
class Product(models.Model):
    name = models.CharField(max_length=500)
    serial = models.CharField(max_length=250, unique=True)
    price = models.DecimalField(max_digits=100, decimal_places=20, default=0.0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.id} {self.name}"
    
    def increase_inventory(self, amount: int):
        from api.models.inventory import Inventory
        """
        Aumenta la cantidad en el inventario del producto.
        
        :param amount: Cantidad a incrementar.
        :type amount: int
        """
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        
        try:
            inventory = Inventory.objects.get(product_id=self)
        except Inventory.DoesNotExist:
            inventory = Inventory.objects.create(product_id=self, count=amount)
        else:
            inventory.count += amount
            inventory.save()