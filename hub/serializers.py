from rest_framework import serializers
from .models import CD, Transaction


class FullCDSerializer(serializers.ModelSerializer):
    cd_url = serializers.CharField(source="get_absolute_url", read_only=True)

    class Meta:
        model = CD
        fields = ['id', 'last_conn', 'ip', 'description', 'region', 'balance', 'cd_url']
        extra_kwargs = {
            "id": {'read_only': True},
            "last_conn": {'read_only': True},
            "balance": {'read_only': True}
        }


class TransactionSerializer(serializers.ModelSerializer):
    model = Transaction
    fields = ['supplier', 'buyer', 'product', 'quantity', 'total']


class RequestCDSerializer(serializers.Serializer):
    product = serializers.CharField()
    quantity = serializers.IntegerField()
    ip = serializers.CharField()