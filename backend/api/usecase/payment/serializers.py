import django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from utils.constants import status as status_payment
from api.models.payment import Payment, PaymentDetail
from api.models.product import Product
from api.usecase.product.serializers import ProductSerializer



class PaymentDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = PaymentDetail
        fields = fields = ['id', 'payment_id', 'product']


class PaymentSerializer(serializers.ModelSerializer):
    payment_details = PaymentDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Payment
        fields = ['id', 'total_amount', 'status', 'payment_details', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total_amount', 'status', 'created_at', 'updated_at']


class PaymentCreatedDraftSerializer(serializers.ModelSerializer):
    payment_details = PaymentDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Payment
        fields = ['id', 'total_amount', 'status', 'payment_details', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total_amount', 'status', 'created_at', 'updated_at']


class PaymentCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'total_amount', 'status', 'created_at', 'updated_at']


def get_product_choices():
    products = Product.objects.all()
    return [f"{product.pk} {product.name}" for product in products]


class PaymentAddDetailSerializer(serializers.ModelSerializer):
    product = serializers.ChoiceField(choices=[], required=True)

    class Meta:
        model = Payment
        fields = ['product']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].choices = self.get_product_choices()
    
    def get_product_choices(self):
        products = Product.objects.all()
        return [f"{product.pk} {product.name}" for product in products]


class PaymentDetailRemoveSerializer(serializers.ModelSerializer):
    payment_detail_id = serializers.CharField()
    
    class Meta:
        model = Payment
        fields = ['payment_detail_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['payment_detail_id']:
            self.fields[field_name].required = True
    

class PaymentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PaymentFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=status_payment.STATUS_PAYMENT, exclude=False)

    class Meta:
        model = Payment
        fields = ['status']

    def filter_queryset(self, queryset):
        for name, value in self.form.cleaned_data.items():
            if value:
                queryset = self.filters[name].filter(queryset, value)
        return queryset
