from django.db import models 

class PaymentDetail(models.Model):
    payment_id = models.ForeignKey('Payment', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True )
    
    def __str__(self) -> str:
        return f"{self.id} - ({self.payment_id}, {self.product_id})"