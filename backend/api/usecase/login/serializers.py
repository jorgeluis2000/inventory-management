from rest_framework import serializers
import django_filters
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(help_text="")
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields =  ['id']
        extra_kwargs = {'password': {'write_only': True}}
        

class UserSerializerCreated(serializers.ModelSerializer):
    username = serializers.CharField(help_text="")
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields =  ['id']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'required': False},
            'email': {'required': False},
        }


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields =  ['id', 'email']
        extra_kwargs = {'password': {'write_only': True}}

class UserLoginRefreshTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains', exclude=False)
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains', exclude=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def filter_queryset(self, queryset):
        for name, value in self.form.cleaned_data.items():
            if value:
                queryset = self.filters[name].filter(queryset, value)
        return queryset