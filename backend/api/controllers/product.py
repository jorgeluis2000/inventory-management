from rest_framework import status, viewsets, permissions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from django.db import IntegrityError
from api.models.inventory import Inventory
from api.usecase.product.serializers import (
    ProductPagination,
    ProductSerializer,
    ProductFilter,
    ProductUpdateSerializer,
    Product
    )
from api.usecase.inventory.serializers import InventoryIncrementSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    
    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action in ['update']:
            return ProductUpdateSerializer
        elif self.action in ['increase_inventory']:
            return InventoryIncrementSerializer
        return ProductSerializer
    
    
    def get_permissions(self):
        if self.action in ['list', 'create', 'update', 'destroy', 'retrieve', 'increase_inventory']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['partial_update']:
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'], url_path='increase_inventory', url_name='increase_inventory')
    def increase_inventory(self, request, pk):
        self.check_permissions(request)
        try:
            product = self.get_object()
            amount = request.data.get('count')
            product.increase_inventory(int(amount))
            return Response({"detail": "Inventory updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"detail": "PATCH method is not allowed for this endpoint."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def update(self, request, *args, **kwargs):
        """
        Custom full update action to handle empty fields and unique serial validation.
        """
        partial = False
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def perform_create(self, serializer):
        try:
            product = serializer.save()
            Inventory.objects.create(product_id=product, count=0)
        except IntegrityError as e:
            return Response(
                {"detail": "A product with this serial number already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return  Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )