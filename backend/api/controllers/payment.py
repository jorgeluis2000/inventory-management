from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models.payment import Payment
from api.models.product import Product
from rest_framework import serializers
from api.usecase.payment.serializers import (PaymentSerializer, PaymentCreatedSerializer,
                                             PaymentPagination, PaymentFilter, PaymentCreatedDraftSerializer, PaymentAddDetailSerializer)
from django_filters.rest_framework import DjangoFilterBackend


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('id')
    serializer_class = PaymentSerializer
    pagination_class = PaymentPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action in ['create']:
            return PaymentCreatedDraftSerializer
        elif self.action in ['add_detail']:
            return PaymentAddDetailSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'add_detail', 'remove_detail', 'cancel', 'mark_as_paid']:
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

    def create(self, request, *args, **kwargs):
        try:
            self.check_permissions(request)
            response_serializer = PaymentCreatedSerializer(data={'status': 1, 'total_amount': 0.0}, partial=True)
            response_serializer.is_valid(raise_exception=True)
            response_serializer.save()
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
        amount = request.data.get('amount')
        try:
            product_id = int(product_value.split()[0])
            product = Product.objects.get(id=product_id)
            payment.add_payment_detail(product, amount)
            return Response({"detail": "Payment detail added successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def remove_detail(self, request, pk=None):
        payment = self.get_object()
        payment_detail_id = request.data.get('payment_detail_id')
        try:
            payment.remove_payment_detail(payment_detail_id)
            return Response({"detail": "Payment detail removed successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        payment = self.get_object()
        try:
            payment.cancel()
            return Response({"detail": "Payment canceled successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        payment = self.get_object()
        try:
            payment.mark_as_paid()
            return Response({"detail": "Payment marked as paid successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
