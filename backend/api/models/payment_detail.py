from django.db import models 
from api.models.payment import Payment
from api.models.product import Product

class PaymentDetail(models.Model):
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.id} - ({self.payment_id}, {self.product_id})"