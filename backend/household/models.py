import math
from django.db import models
from django.contrib.auth.models import User
from locations.models import Region, District, Ward, VillageStreet, Hamlet


class HamletHouseholdExpectation(models.Model):
    hamlet = models.ForeignKey(
        Hamlet,
        on_delete=models.CASCADE,
        related_name='household_expectations'
    )
    expected_households = models.PositiveIntegerField(default=0)
    availabled_households = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hamlet.name} - Expected Households: {self.expected_households}"
    
class Household(models.Model):
    household_head_name = models.CharField(max_length=255)
    number_of_men = models.PositiveIntegerField(default=0)
    number_of_women = models.PositiveIntegerField(default=0)
    household_head_phone_number = models.CharField(max_length=20)
    village_street = models.CharField(max_length=255)

    # Location fields
    region = models.ForeignKey(Region, on_delete=models.CASCADE, default=1)
    district = models.ForeignKey(District, on_delete=models.CASCADE, default=1)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, default=1)
    village = models.ForeignKey(VillageStreet, on_delete=models.CASCADE, default=1)
    hamlet = models.ForeignKey(Hamlet, on_delete=models.CASCADE, default=1)

    # VEO user
    veo = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=1)

    @property
    def total_members(self):
        return self.number_of_men + self.number_of_women

    @property
    def number_net_needed(self):
        """Always round up to nearest whole number"""
        return math.ceil(self.total_members / 2)

    def __str__(self):
        return f"{self.household_head_name} - {self.veo.username if self.veo else 'N/A'}"
