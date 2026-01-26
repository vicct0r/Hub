from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db import transaction

from .serializers import FullCDSerializer
from .models import CD


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

