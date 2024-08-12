from django.db import models 

class PaymentDetail(models.Model):
    payment_id = models.ForeignKey('Payment', db_column='payment_id', help_text='Referencia al pago asociado.' ,on_delete=models.CASCADE, related_name='payment_details')
    # product_id = models.ForeignKey('Product', db_column='product_id', help_text='Referencia al producto asociado.' ,on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Product', db_column='product_id', help_text='Referencia al producto asociado.' ,on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'payment_detail'
        
    def __str__(self) -> str:
        return f"{self.id} - ({self.payment_id}, {self.product})"