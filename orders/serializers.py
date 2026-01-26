from rest_framework import serializers

from .models import Order
from catalog.models import Product
from hub.models import CD


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'created', 'modified', 'status', 'client']


class OrderCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['sku', 'quantity', 'client']
        
    def create(self, validated_data):
        product = Product.objects.get(sku=validated_data['sku'])
        client = CD.objects.get(id=client)
        insufficient_batch = product.quantity < validated_data['quantity']

        if insufficient_batch:
            status = Order.AWAITING_CUSTOMER_DECISION
        else:
            status = Order.CONFIRMED
        
        return Order.objects.create(
            product=product,
            quantity=validated_data['quantity'],
            total_price=validated_data['quantity'] * product.price,
            client=client.id,
            status=status
        )
    
    