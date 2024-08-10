from django.urls import path, include
from rest_framework import routers
from api.controllers.login import LoginViewSet
from api.controllers.product import ProductViewSet

CrudRouter = routers.DefaultRouter()
CrudRouter.register(r'credentials', viewset=LoginViewSet)
CrudRouter.register(r'products', viewset=ProductViewSet)

urlpatterns = [
    path('', include(CrudRouter.urls)),
]