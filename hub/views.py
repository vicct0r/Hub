from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db import transaction

import requests

from .serializers import FullCDSerializer, RequestCDSerializer, TransactionSerializer
from .models import CD, Transaction


class CdListCreateAPIView(generics.ListCreateAPIView):
    """
    **POST** Distribution Center **creation** objects endpoint
    - **Full serializer** with models.Base fields
    """
    queryset = CD.objects.all()
    serializer_class = FullCDSerializer

    def get_queryset(self):
        return CD.objects.all().order_by("id")

class CdRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CD.objects.all()
    serializer_class = FullCDSerializer

    def get_object(self):
        if self.kwargs.get('id'):
            return get_object_or_404(self.queryset, id=self.kwargs.get('id'))
        elif self.kwargs.get('slug'):
            return get_object_or_404(self.queryset, slug=self.kwargs.get('slug'))


class CdRequestAPIView(APIView):
    """
    **POST** - Transaction trade for Distribution Centers
    - CDs trade products trough this endpoint
    - Buyer CD will request this endpoint to ask HUB for more products
    - HUB will gather all candidates, choosing the cheaper one
    - HUB validates and operate the trade between the CD actors
    """
    def post(self, request, *args, **kwargs):
        serializer = RequestCDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        product = data['product']
        quantity = data['quantity']
        ip = data['ip']

        supliers = {}
        available_supliers = CD.objects.exclude(ip=ip)

        try:
            for unity in available_supliers:
                
                if unity.ip == ip:
                    continue

                response = requests.get(
                url = f"http://{unity.ip}/cd/v1/product/request/{product}/{quantity}/",
                timeout=5
                )

                response.raise_for_status()

                if response.status_code != 200:
                    continue

                _data = response.json()

                supliers[str(unity.id)] = {
                    "ip": unity.ip,
                    "id": _data["id"],
                    "total_price": _data["total_price"]
                }

        except Exception as e:
            return Response({
                "status": "success",
                "error_msg": f"{str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "status": "code",
            "supliers": supliers,
            "action": "report"
        }, status=status.HTTP_200_OK)        


class TransactionsListAPIView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all().order_by("id")


class TransactionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'id'

