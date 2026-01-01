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
    queryset = CD.objects.filter(is_active=True)
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
        cds = CD.objects.filter(is_active=True).exclude(ip=ip)
        seller = {}
        
        try:
            for cd in cds:
                try:
                    cd_response = requests.get(
                    url = f"http://{cd.ip}/cd/v1/product/request/{product}/{quantity}/",
                    timeout=5
                    )
                except Exception as e:
                    print(str(e))
                       
                cd_response.raise_for_status()
                data = cd_response.json()

                if data['available'] != "true":
                    continue

                if seller:
                    if data['price'] < seller['price']:
                        seller = {"cd": cd.name, "price": data['price'], "quantity": data['quantity']}
                else:
                    seller = {"cd": cd.name, "price": data['price'], "quantity": data['quantity']}
            
            if not seller:
                return Response({
                    "status": "error",
                    "message": f"Could not find any CD with the requested amount of {product}"
                }, status=status.HTTP_200_OK)

            transaction_price = seller['price'] * quantity

            transaction_data = {
                "product": product,
                "quantity": quantity
            }

            try:
                with transaction.atomic(): # contendo todo o processo de concorrencia dentro da operacao
                    suplier = CD.objects.select_for_update().get(name=seller['cd'])
                    buyer = CD.objects.select_for_update().get(ip=ip)

                    target_url = f"http://{suplier.ip}/cd/v1/product/sell/"
                    origin_url = f"http://{buyer.ip}/cd/v1/product/buy/"
                    
                    print(f"SUPLIER: {suplier.name}-{suplier.ip}\nBUYER: {buyer.name}-{buyer.ip}")

                    target_response = requests.post(
                        url=target_url,
                        json=transaction_data,
                        timeout=5
                    )
                    target_response.raise_for_status()

                    origin_response = requests.post(
                        url=origin_url,
                        json=transaction_data,
                        timeout=5
                    )
                    origin_response.raise_for_status()

                    if target_response.status_code == 200 and origin_response.status_code == 200:
                        suplier.balance += transaction_price
                        buyer.balance -= transaction_price
                        suplier.save()
                        buyer.save()
                        
                        Transaction.objects.create(
                            supplier=suplier,
                            buyer=buyer,
                            product=product,
                            quantity=quantity,
                            total=transaction_price
                        )

                        return Response({
                            "status": "success",
                            "product": product,
                            "quantity": quantity,
                            "buyer": buyer.name,
                            "suplier": suplier.name,
                            "action": "trade"
                        }, status=status.HTTP_200_OK)                
                    else:
                        return Response({
                            "status": "error",
                            "message": "Something went wrong with the transaction!",
                            "error_msg_origin": origin_response.raise_for_status,
                            "error_msg_target": target_response.raise_for_status,
                            "msg": str(e)
                        }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    "status": "error",
                    "message": "Something went wrong!",
                    "error_msg": str(e)
                }, status=status.HTTP_424_FAILED_DEPENDENCY)
        except Exception as e:
            return Response({
                "status": "error",
                "error_msg": str(e),
            }, status=status.HTTP_400_BAD_REQUEST)


class TransactionsListAPIView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all().order_by("id")


class TransactionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'id'    

