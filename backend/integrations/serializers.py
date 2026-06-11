from rest_framework import serializers
from .models import Integration


class IntegrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Integration

        fields = [
            'id',
            'provider',
            'access_token',
            'refresh_token',
            'realm_id',
            'is_active',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]