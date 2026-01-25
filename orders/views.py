from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer, ClientIdentifierSerializer
from catalog.models import Product
from hub.models import CD

class OrderListAPIView(APIView):
    # precisamos saber qual CD está pedindo pela lista de Pedidos.
    # por enquanto, não poderá ser GET

    def post(self, request, *args, **kwargs):
        serializer = ClientIdentifierSerializer(data=request.data)
        data = serializer.validated_data(raise_exceptions=True)

        client = CD.objects.get(id=data['client_id'])

        if client:
            client_orders = Order.objects.filter(id=data['client_id'])
            return Response({
                "status": "success",
                "orders": client_orders
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "error",
                "error_msg": "client id not found."
            }, status=status.HTTP_404_NOT_FOUND)
        

class OrderCreateAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        data = serializer.validated_data(raise_exceptions=True)

        product = Product.objects.get(sku=data['sku'])

        if product:
            _requested_quantity = data['quantity']

            if product.quantity < _requested_quantity:
                order = Order.objects.create(
                    client = data['client']
                )

                return Response({
                    "status": "success",
                    "message": "not enought products to fullfill the batch.",
                    "info": "please choose the operational solution for the trade request on the order URL.",
                    "url": order.get_absolute_url()
                }, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('id')
        order = Order.objects.get(id=order_id)

        if not order:
            return Response({
                "status": "not found",
                "message": "order does not exist.",
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
                "id": order.id,
                "created_at": order.created,
                "modified": order.modified,
                "client": order.client,
                "product": order.product,
                "quantity": order.quantity,
                "total_price": order.total_price
            }, status=status.HTTP_200_OK)

        
