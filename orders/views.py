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
        data = serializer.validated_data

        product = get_object_or_404(Product, sku=data['sku'])
        client = get_object_or_404(CD, id=data['client'])
        insufficient_bath_quantity = product.quantity < data['quantity']

        if insufficient_bath_quantity:

            order = Order.objects.create(
                client=client,
                status=Order.AWAITING_CUSTOMER_DECISION,
                product=product,
                quantity=data['quantity'],
                total_price=data['quantity'] * product.price
            )

            return Response({
                "status": "success",
                "message": "not enought products to fullfill the batch.",
                "info": "please choose the operational solution for the trade request on the order URL.",
                "url": order.get_absolute_url()
            }, status=status.HTTP_202_ACCEPTED)


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

        
