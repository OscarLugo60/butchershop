from rest_framework import serializers
from .models import CarShop
from applications.producto.serializers import ProductSerializer

class CarListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CarShop
        fields = [
            'id',
            'product',
            'count',
        ]

class CarUpdateSerilizer(serializers.ModelSerializer):
    class Meta:
        model = CarShop
        fields = ['count',]