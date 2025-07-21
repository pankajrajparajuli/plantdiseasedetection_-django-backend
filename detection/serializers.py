# serializers.py
from rest_framework import serializers
from .models import PredictionHistory


class PredictionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionHistory
        fields = ['id', 'image', 'disease', 'confidence', 'remedy', 'timestamp']
        read_only_fields = ['timestamp']
