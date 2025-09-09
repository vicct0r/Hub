from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
import requests

from .serializers import FullCDSerializer, RequestCDSerializer
from .models import CD


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

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
            port = request.META.get("REMOTE_PORT")
        
        formated_ip = f"{ip}" if not port else f"{ip}:{port}" # a porta nao esta sendo capturada corretamente
        try:
            for cd in cds:
                if cd.ip == formated_ip:
                    print('IP da API de ORIGEM: ', formated_ip)
                    continue

                try:
                    cd_response = requests.get(
                    url = f"http://{cd.ip}/cd/v1/product/request/{product}/{quantity}/",
                    timeout=5
                    )
                except Exception as e:
                    print(str(e))
                       

                print("Payload enviado ao HUB:")
                print("Resposta do CD:", cd_response.status_code, cd_response.text)
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
            
            print("IP FORMATADO", formated_ip)
            print("SELLER: ", seller)
            suplier = get_object_or_404(CD, name=seller['cd'])
            buyer = get_object_or_404(CD, ip=formated_ip)

            target_url = f"http://{suplier.ip}/cd/v1/product/sell/"
            origin_url = f"http://{buyer.ip}/cd/v1/product/buy/"
            print(f"SUPLIER: {suplier.name}-{suplier.ip}\nBUYER: {buyer.name}-{buyer.ip}")
            transaction_data = {
                "product": product,
                "quantity": quantity
            }

            try:
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
            except Exception as e:
                return Response({
                    "status": "error",
                    "message": "Something went wrong!",
                    "error_msg": str(e)
                }, status=status.HTTP_424_FAILED_DEPENDENCY)

            if target_response.status_code == 200 and origin_response.status_code == 200:
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
                "error_msg": str(e),
            }, status=status.HTTP_400_BAD_REQUEST)