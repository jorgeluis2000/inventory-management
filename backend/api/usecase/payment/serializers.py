import django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from utils.constants import status as status_payment
from api.models.payment import Payment
from api.models.product import Product


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'total_amount', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentCreatedDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'total_amount', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total_amount', 'status', 'created_at', 'updated_at']


class PaymentCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'total_amount', 'status' 'created_at', 'updated_at']


def get_product_choices():
    products = Product.objects.all()
    return [f"{product.pk} {product.name}" for product in products]


class PaymentAddDetailSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(default=0)
    product = serializers.ChoiceField(choices=get_product_choices())

    class Meta:
        model = Payment
        fields = ['amount', 'product']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['amount', 'product']:
            self.fields[field_name].required = True


class PaymentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PaymentFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        field_name='status', lookup_expr='icontains', choices=status_payment.STATUS_PAYMENT, exclude=False)

    class Meta:
        model = Payment
        fields = ['status']

    def filter_queryset(self, queryset):
        for name, value in self.form.cleaned_data.items():
            if value:
                queryset = self.filters[name].filter(queryset, value)
        return queryset
