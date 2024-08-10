from rest_framework import status, viewsets, permissions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from api.models.product import Product
from api.usecase.product.serializers import (
    ProductPagination,
    ProductSerializer,
    ProductFilter,
    ProductUpdateSerializer
    )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
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
        return ProductSerializer
    
    
    def get_permissions(self):
        if self.action in ['list', 'create', 'update', 'destroy', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['partial_update']:
            return [permissions.AllowAny()]
        return super().get_permissions()
    
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