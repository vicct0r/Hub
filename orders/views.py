from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer, ClientListOrderSerializer
from catalog.models import Product
from hub.models import CD

class OrderListAPIView(APIView):
    # precisamos saber qual CD está pedindo pela lista de Pedidos.
    # por enquanto, não poderá ser GET

    def post(self, request, *args, **kwargs):
        serializer = ClientListOrderSerializer(data=request.data)
        serializer.is_valid(raise_exceptions=True)
        data = serializer.save()

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
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response({
            "status": "success",
            "order_id": order.id,
            "order_status": order.status,
            "order_url": order.get_absolute_url(),
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

        
