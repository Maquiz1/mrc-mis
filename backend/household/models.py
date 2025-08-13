from django.db import models
from django.contrib.auth.models import User

class Household(models.Model):
    household_head_name = models.CharField(max_length=100)
    number_of_men = models.PositiveIntegerField(null=True, blank=True)
    number_of_women = models.PositiveIntegerField(null=True, blank=True)
    household_head_phone_number = models.CharField(max_length=15)
    village_street = models.CharField(max_length=150)
    veo = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def total_members(self):
        men = self.number_of_men or 0
        women = self.number_of_women or 0
        return men + women

    def __str__(self):
        return f"{self.household_head_name} - {self.veo.username}"
