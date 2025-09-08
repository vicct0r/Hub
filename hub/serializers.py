from rest_framework import serializers
from .models import CD


class FullCDSerializer(serializers.ModelSerializer):
    class Meta:
        model = CD
        fields = ['id', 'created', 'modified', 'is_active', 'last_conn', 'name', 'ip', 'description', 'region', 'balance']
        extra_kwargs = {
            "id": {'read_only': True},
            "created": {'read_only': True},
            "modified": {'read_only': True},
            "is_active": {'read_only': True},
            "last_conn": {'read_only': True},
            "balance": {'read_only': True}
        }


class RequestCDSerializer(serializers.Serializer):
    product = serializers.CharField()
    quantity = serializers.IntegerField()
