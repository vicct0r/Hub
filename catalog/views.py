from django.shortcuts import render
from rest_framework import generics

from .serializers import CatalogSerializer
from .models import Product

# acesso publico
class CatalogListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CatalogSerializer
    queryset = Product.objects.filter(available=True)
    lookup_field = 'id'

# acesso restrito para admin
class CatalogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CatalogSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'

# acesso publico
class CatalogRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CatalogSerializer
    queryset = Product.objects.filter(available=True)
    lookup_url_kwarg = 'slug'


