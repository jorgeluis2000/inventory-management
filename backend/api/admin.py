from django.contrib import admin
from api.models.payment_detail import PaymentDetail
from api.models.payment import Payment
from api.models.inventory import Inventory
from api.models.product import Product

# Register your models here.

admin.site.register(Inventory)
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(PaymentDetail)