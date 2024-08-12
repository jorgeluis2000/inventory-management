from django.test import TestCase
from decimal import Decimal
from api.models.payment import Payment
from utils.constants import status

class PaymentModelTests(TestCase):

    def setUp(self):
        self.payment = Payment.objects.create(
            total_amount=Decimal('100.00'),
            status=status.STATUS_PAYMENT[0][0]
        )

    def test_create_payment(self):
        """
        Verificar que se crea correctamente un objeto Payment
        """
        self.assertEqual(self.payment.total_amount, Decimal('100.00'))
        self.assertEqual(self.payment.status, status.STATUS_PAYMENT[0][0])
        self.assertIsNotNone(self.payment.created_at)
        self.assertIsNotNone(self.payment.updated_at)

    def test_update_payment(self):
        """
        Actualizar el objeto Payment
        """
        self.payment.total_amount = Decimal('150.00')
        self.payment.save()

        updated_payment = Payment.objects.get(id=self.payment.id)
        self.assertEqual(updated_payment.total_amount, Decimal('150.00'))

    def test_string_representation(self):
        """
        Verificar la representación en cadena del objeto Payment
        """
        self.assertEqual(str(self.payment), f"{self.payment.id} - {self.payment.status}")

    def test_default_status(self):
        """
        Crear un objeto Payment con el estado por defecto
        """
        payment = Payment.objects.create(total_amount=Decimal('200.00'))
        self.assertEqual(payment.status, status.STATUS_PAYMENT[0][0])

    def test_status_choices(self):
        """
        Verificar que las opciones de estado están bien definidas
        """
        choices = dict(status.STATUS_PAYMENT)
        self.assertTrue(len(choices) > 0, "El conjunto de opciones para status está vacío")
        self.assertIn(self.payment.status, choices.keys())
