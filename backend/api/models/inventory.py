from django.db import models 
from api.models.product import Product
class Inventory(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL)
    count = models.BigIntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.id} - {self.product_id.name}"