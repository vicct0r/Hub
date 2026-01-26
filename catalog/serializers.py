from rest_framework import serializers
from .models import Product


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'created', 'modified', 'available']