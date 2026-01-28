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
    sku = serializers.CharField(write_only=True)
    order_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['sku', 'quantity', 'client']
        read_only_fields = ['id', 'sku', 'total_price', 'order_url']

    def create(self, validated_data):
        product = Product.objects.get(sku=validated_data['sku'])
        client = CD.objects.get(id=validated_data['client'])
        insufficient_batch = product.quantity < validated_data['quantity']

        if insufficient_batch:
            status = Order.AWAITING_CUSTOMER_DECISION
        else:
            status = Order.CONFIRMED
        
        return Order.objects.create(
            product=product,
            quantity=validated_data['quantity'],
            total_price=validated_data['quantity'] * product.price,
            client=client,
            status=status
        )
    
    def get_order_url(self, obj):
        return obj.get_absolute_url()


class BatchOperationalChoice(serializers.Serializer):
    class Meta:
        model = Order
        fields = ['operation']
