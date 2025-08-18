from rest_framework import serializers
from ..models import HamletHouseholdExpectation

class HamletHouseholdExpectationSerializer(serializers.ModelSerializer):
    hamlet_name = serializers.CharField(source='hamlet.name', read_only=True)
    
    class Meta:
        model = HamletHouseholdExpectation
        fields = ['id', 'hamlet', 'hamlet_name', 'expected_households', 'reached_households']
