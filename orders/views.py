from django.shortcuts import render, get_object_or_404
from rest_framework import generics

from .models import Order
from .serializers import OrderSerializer, OrderCreationSerializer
from catalog.models import Product
from hub.models import CD

# restrito
class OrderListCreateAPIView(generics.ListCreateAPIView):
    serilizer_class = OrderCreationSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'

# restrito
class OrderRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDeleteAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'

# publico
class OrderRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.exclude(status__in=[Order.COMPLETED, Order.REJECTED])
    lookup_field = 'id'


# batchOperationalChoice
# Endpoint para cliente aceitar lote com qtd atual ou esperar lote completo (será preciso fazer uso de datas)
# Somente o dono do Pedido poderá escolher a operação
