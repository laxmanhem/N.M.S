from rest_framework import serializers
from .models import NetworkLog

class NetworkLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkLog
        fields = '__all__'
