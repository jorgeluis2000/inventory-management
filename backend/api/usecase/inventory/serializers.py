from rest_framework import serializers
from api.models.inventory import Inventory

class InventoryIncrementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'count']
        read_only_fields =  ['id']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['count']:
            self.fields[field_name].required = True