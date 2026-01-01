from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db import transaction

import requests

from .serializers import FullCDSerializer, RequestCDSerializer, TransactionSerializer
from .models import CD, Transaction
from ..cd_client import HUBClient
from .services.Hub import HubService

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
        cds = CD.objects.filter(is_active=True)
        seller = None

        try:
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR") # nao consegui capturar o IP:Porta, somente IP
            if x_forwarded_for:
                ip = x_forwarded_for.split(",")[0].strip()
            else:
                ip = request.META.get("REMOTE_ADDR")
            
            client = get_object_or_404(CD, ip=ip)
            trade_response = HubService.trade_request(client=client)

            # isso realmente faz parte de um só processo? 
            # buscar_candidato -> selecionar_candidato -> (transacao entre cliente e fornecedor [CDs]) -> devolver_resposta
             
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

