# detection/serializers.py
from rest_framework import serializers
from .models import PredictionHistory

class PredictionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionHistory
        fields = '__all__'
