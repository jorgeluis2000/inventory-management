from django.db import models 
from utils.constants import status as status_payment
from .payment_detail import PaymentDetail

class Payment(models.Model):
    total_amount = models.DecimalField(
        max_digits=100, 
        decimal_places=20, 
        db_column='total_amount',
        help_text='Total amount of the payment'
    )
    status = models.PositiveSmallIntegerField(
        default=1, 
        choices=status_payment.STATUS_PAYMENT, 
        db_column='status',
        help_text='Current status of the payment'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        db_column='created_at',
        help_text='Time when the payment was created'
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        db_column='updated_at',
        help_text='Time when the payment was last updated'
    )
    
    class Meta:
        db_table = 'payment'
    
    def __str__(self) -> str:
        return f"{self.id} - {self.status}"