from django.db import models 
from utils.constants import status

class Payment(models.Model):
    total_amount = models.DecimalField(max_digits=100, decimal_places=20)
    status = models.PositiveSmallIntegerField(default=1, choices=status.STATUS_PAYMENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.id} - {self.status}"