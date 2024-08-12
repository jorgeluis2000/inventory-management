from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models.payment import Payment
from api.models.product import Product
from rest_framework import serializers
from api.usecase.payment.serializers import (PaymentSerializer, PaymentCreatedSerializer, PaymentDetailRemoveSerializer,
                                             PaymentPagination, PaymentFilter, PaymentCreatedDraftSerializer, PaymentAddDetailSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from utils.functions.procedures import create_payment, add_payment_detail, remove_payment_detail, cancel_payment, delete_cancelled_payments, mark_payment_as_paid, delete_cancelled_payments


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-created_at')
    serializer_class = PaymentSerializer
    pagination_class = PaymentPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

    def get_serializer_class(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update', 'delete_cancelled_payments', 'cancel', 'mark_as_paid']:
            return PaymentCreatedDraftSerializer
        elif self.action in ['add_detail']:
            return PaymentAddDetailSerializer
        elif self.action in ['remove_detail']:
            return PaymentDetailRemoveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'add_detail', 'remove_detail', 'cancel', 'mark_as_paid', 'delete_cancelled_payments']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"detail": "PATCH method is not allowed for this endpoint."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "PUT method is not allowed for this endpoint."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
        
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "DELETE method is not allowed for this endpoint."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        try:
            payment_id = create_payment()
            payment = Payment.objects.get(id=payment_id)
            response_serializer = PaymentCreatedSerializer(payment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "An error occurred while creating the payment."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def add_detail(self, request, pk=None):
        self.check_permissions(request)
        payment = self.get_object()
        product_value = request.data.get('product')
        try:
            product_id = int(product_value.split()[0])
            add_payment_detail(payment_id=payment.id, product_id=product_id, quantity=1)
            return Response({"detail": "Payment detail added successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def remove_detail(self, request):
        payment_detail_id = request.data.get('payment_detail_id')
        try:
            remove_payment_detail(int(payment_detail_id))
            return Response({"detail": "Payment detail removed successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        payment = self.get_object()
        try:
            cancel_payment(payment_id=int(payment.pk))
            payment.refresh_from_db()
            return Response({"detail": "Payment canceled successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['delete'])
    def delete_cancelled_payments(self, request, pk=None):
        payment = self.get_object()
        try:
            delete_cancelled_payments(payment_id=int(payment.pk))
            payment.refresh_from_db()
            return Response({"detail": "Payment deleted successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        payment = self.get_object()
        try:
            mark_payment_as_paid(payment_id=int(payment.pk))
            return Response({"detail": "Payment marked as paid successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
