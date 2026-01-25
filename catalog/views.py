from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView

from .serializers import CatalogSerializer
from .models import Product

class CatalogListAPIView(generics.ListAPIView):
    serializer_class = CatalogSerializer
    queryset = Product.objects.filter(available=True)
