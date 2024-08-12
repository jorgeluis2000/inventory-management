from django.db import models 
class Inventory(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        db_column='product_id',
        help_text='Referencia al producto asociado.'
    )
    count = models.BigIntegerField(
        default=0,
        db_column='count',
        help_text='Cantidad en inventario.'
    )
    
    class Meta:
        db_table = 'inventory'
    
    def __str__(self) -> str:
        return f"{self.id} - ({self.product}) - {self.count}"