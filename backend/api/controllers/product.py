from rest_framework import status, viewsets, permissions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from api.models.product import Product
from api.usecase.product.serializers import ProductPagination, ProductSerializer, ProductFilter


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    
    
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