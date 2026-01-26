from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .serializers import FullClientSerializer
from .models import CD


class ClientCreateAPIView(generics.CreateAPIView):
    serializer_class = FullClientSerializer
    queryset = CD.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "status": "success",
            "operation": "service_creation",
            "client": response.data
        }, status=response.status_code)


class ClientListAPIView(generics.ListAPIView):
    """
    **POST** Distribution Center **creation** objects endp
    
    """
    queryset = CD.objects.all()
    serializer_class = FullClientSerializer

    def get_queryset(self):
        return CD.objects.all().order_by("id")


class CdRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CD.objects.all()
    serializer_class = FullClientSerializer

    def get_object(self):
        if self.kwargs.get('id'):
            return get_object_or_404(self.queryset, id=self.kwargs.get('id'))
        elif self.kwargs.get('slug'):
            return get_object_or_404(self.queryset, slug=self.kwargs.get('slug'))
