from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from .serializers import FullClientSerializer
from .models import CD

# restrito
class ClientListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FullClientSerializer
    queryset = CD.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "status": "success",
            "operation": "client_submition",
            "client": response.data
        }, status=response.status_code)

# restrito
class CdRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CD.objects.all()
    serializer_class = FullClientSerializer

    def get_object(self):
        if self.kwargs.get('id'):
            return get_object_or_404(self.queryset, id=self.kwargs.get('id'))
        elif self.kwargs.get('slug'):
            return get_object_or_404(self.queryset, slug=self.kwargs.get('slug'))
