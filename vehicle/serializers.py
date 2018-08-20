# REST framework
from rest_framework import serializers

# Project
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = (
            'vin', 'year', 'make', 'model', 'type',
            'color', 'dimensions', 'weight'
        )
