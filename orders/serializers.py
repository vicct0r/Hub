from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.Serializer):
    client = serializers.IntegerField()
    sku = serializers.CharField()
    quantity = serializers.IntegerField()


class ClientIdentifierSerializer(serializers.Serializer):
    client_id = serializers.UUIDField()
