from rest_framework import serializers
from .models import HamletHouseholdExpectation, Household
from locations.models import Hamlet

class HamletHouseholdExpectationSerializer(serializers.ModelSerializer):
    hamlet_name = serializers.CharField(source='hamlet.name', read_only=True)
    
    class Meta:
        model = HamletHouseholdExpectation
        fields = ['id', 'hamlet', 'hamlet_name', 'expected_households', 'reached_households']

class HouseholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = '__all__'