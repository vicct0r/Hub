from rest_framework import serializers
from .models import CD


class FullClientSerializer(serializers.ModelSerializer):
    cd_url = serializers.CharField(source="get_absolute_url", read_only=True)

    class Meta:
        model = CD
        fields = '__all__'
        read_only_fields = ['created', 'modified', 'is_active', 'id', 'slug']

