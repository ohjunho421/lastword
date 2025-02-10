from rest_framework import serializers
from .models import Recommendation, LottoData

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'draw_number', 'recommended_numbers', 'match_count', 'created_at']

class LottoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LottoData
        fields = ['draw_number', 'num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'bonus_number']