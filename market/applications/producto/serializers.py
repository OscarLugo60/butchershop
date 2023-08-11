from rest_framework import serializers, pagination
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'code',
            'name',
            'count',
            'get_unit_display',
            'sale_price'
        )