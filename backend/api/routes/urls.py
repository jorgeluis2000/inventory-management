from django.urls import path, include
from rest_framework import routers
from api.controllers.login import LoginViewSet
from api.controllers.product import ProductViewSet
from api.controllers.payment import PaymentViewSet

CrudRouter = routers.DefaultRouter()
CrudRouter.register(r'credentials', viewset=LoginViewSet, basename='credentials')
CrudRouter.register(r'products', viewset=ProductViewSet, basename='products')
CrudRouter.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('', include(CrudRouter.urls)),
]