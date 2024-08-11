from django.db import models 
from utils.constants import status as status_payment
from .payment_detail import PaymentDetail

class Payment(models.Model):
    total_amount = models.DecimalField(max_digits=100, decimal_places=20)
    status = models.PositiveSmallIntegerField(default=1, choices=status_payment.STATUS_PAYMENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.id} - {self.status}"
    
    def add_payment_detail(self, product, amount):
        if self.status != 1:
            raise ValueError("Cannot add details to a non-draft payment.")
        PaymentDetail.objects.create(payment_id=self, product_id=product)
        self.total_amount += amount
        self.save()

    def remove_payment_detail(self, payment_detail_id: int):
        """Elimina un payment detail y actualiza el monto total del pago.

        Args:
            payment_detail_id (int): id del detalle a eliminar

        Raises:
            ValueError: El estado del payment no es "draft"
        """
        if self.status != 1:
            raise ValueError("Cannot remove details from a non-draft payment.")
        payment_detail = PaymentDetail.objects.get(id=payment_detail_id, payment_id=self)
        self.total_amount -= payment_detail.product_id.price
        payment_detail.delete()
        self.save()

    def cancel(self):
        if self.status != 1:
            raise ValueError("Cannot cancel a non-draft payment.")
        self.status = 2
        self.save()

    def mark_as_paid(self):
        if self.status != 1:
            raise ValueError("Cannot mark as paid for a non-draft payment.")
        self.status = 3
        self.save()
        for detail in PaymentDetail.objects.filter(payment_id=self):
            product = detail.product_id
            product.inventory.count -= 1
            product.inventory.save()