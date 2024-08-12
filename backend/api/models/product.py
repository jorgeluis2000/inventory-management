from django.db import models 
class Product(models.Model):
    name = models.CharField(
        max_length=500, 
        db_column='name',
        help_text='Name of the product'
    )
    serial = models.CharField(
        max_length=250, 
        unique=True, 
        db_column='serial',
        help_text='Unique serial number of the product'
    )
    price = models.DecimalField(
        max_digits=100, 
        decimal_places=20, 
        default=0.0, 
        db_column='price',
        help_text='Price of the product'
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        db_column='updated_at',
        help_text='Time when the product was last updated'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        db_column='created_at',
        help_text='Time when the product was created'
    )
    
    class Meta:
        db_table = 'product'
    
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
            inventory = Inventory.objects.get(product_id=self.pk)
        except Inventory.DoesNotExist:
            inventory = Inventory.objects.create(product_id=self.pk, count=amount)
        else:
            inventory.count += amount
            inventory.save()