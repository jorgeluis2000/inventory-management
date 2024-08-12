from decimal import Decimal
from django.test import TestCase
from api.models.payment import Payment
from api.models.product import Product
from api.models.payment_detail import PaymentDetail
from utils.constants import status

class PaymentDetailModelTests(TestCase):

    def setUp(self):
        self.payment = Payment.objects.create(
            total_amount=Decimal('100.00'),
            status=status.STATUS_PAYMENT[0][0]
        )
        self.product = Product.objects.create(
            name='Test Product',
            serial='1234567890',
            price=Decimal('10.00')
        )
        
        self.payment_detail = PaymentDetail.objects.create(
            payment_id=self.payment,
            product_id=self.product
        )

    def test_create_payment_detail(self):
        """
        Verificar que se crea correctamente un objeto PaymentDetail
        """
        self.assertEqual(self.payment_detail.payment_id, self.payment)
        self.assertEqual(self.payment_detail.product_id, self.product)

    def test_string_representation(self):
        """
        Verificar la representación en cadena del objeto PaymentDetail
        """
        expected_str = f"{self.payment_detail.id} - ({self.payment}, {self.product})"
        self.assertEqual(str(self.payment_detail), expected_str)

    def test_update_payment_detail(self):
        """
        Crear otro objeto Product para actualizar
        """
        new_product = Product.objects.create(
            name='Another Product',
            serial='0987654321',
            price=Decimal('20.00')
        )

        self.payment_detail.product_id = new_product
        self.payment_detail.save()

        updated_payment_detail = PaymentDetail.objects.get(id=self.payment_detail.id)
        self.assertEqual(updated_payment_detail.product_id, new_product)

    def test_foreign_key_relationships(self):
        """
        Verificar las relaciones de clave externa
        """
        self.assertEqual(self.payment_detail.payment_id, self.payment)
        self.assertEqual(self.payment_detail.product_id, self.product)

    def test_str_with_no_objects(self):
        """
        Crear un objeto PaymentDetail sin objetos Payment y Product
        """
        empty_payment = Payment.objects.create(
            total_amount=Decimal('0.00'),
            status=status.STATUS_PAYMENT[0][0]
        )
        empty_product = Product.objects.create(
            name='Empty Product',
            serial='0000000000',
            price=Decimal('0.00')
        )
        empty_payment_detail = PaymentDetail.objects.create(
            payment_id=empty_payment,
            product_id=empty_product
        )

        expected_str = f"{empty_payment_detail.id} - ({empty_payment}, {empty_product})"
        self.assertEqual(str(empty_payment_detail), expected_str)
