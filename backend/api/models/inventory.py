from django.db import models 
class Inventory(models.Model):
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    count = models.BigIntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.id} - ({self.product_id}) - {self.count}"