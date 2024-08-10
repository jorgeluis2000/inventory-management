import django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from api.models.product import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'serial', 'price', 'updated_at', 'created_at']
        read_only_fields =  ['id', 'created_at', 'updated_at']
 
class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'serial', 'price', 'updated_at', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['name', 'serial', 'price']:
            self.fields[field_name].required = False
    
    def validate(self, data):
        if 'serial' in data:
            if Product.objects.filter(serial=data['serial']).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({'serial': 'This serial number already exists.'})
        return data
class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
        
class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', exclude=False)
    serial = django_filters.CharFilter(field_name='serial', lookup_expr='icontains', exclude=False)
    class Meta:
        model = Product
        fields = ['name', 'serial']

    def filter_queryset(self, queryset):
        for name, value in self.form.cleaned_data.items():
            if value:
                queryset = self.filters[name].filter(queryset, value)
        return queryset