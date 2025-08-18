from rest_framework import generics
from ..models import HamletHouseholdExpectation
from .serializers import HamletHouseholdExpectationSerializer

class HouseholdListCreateAPIView(generics.ListCreateAPIView):
    queryset = HamletHouseholdExpectation.objects.all()
    serializer_class = HamletHouseholdExpectationSerializer

class HouseholdRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = HamletHouseholdExpectation.objects.all()
    serializer_class = HamletHouseholdExpectationSerializer
