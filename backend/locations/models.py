# locations/models.py

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class AuditModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created"
    )

    updated_at = models.DateTimeField(auto_now=True)

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated"
    )

    class Meta:
        abstract = True


class Country(AuditModel):
    name = models.CharField(max_length=100)
    # code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class Region(AuditModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE,related_name="regions")
    name = models.CharField(max_length=100)
    # code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class District(AuditModel):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,related_name="districts"
)

    def __str__(self):
        return f"{self.name}, {self.region.name}"


class Site(AuditModel):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE,related_name="sites"
)

    def __str__(self):
        return f"{self.name} - {self.district.name}"


class Ward(AuditModel):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE,related_name="wards")

    def __str__(self):
        return f"{self.name}, {self.district.name}"


class VillageStreet(AuditModel):  # Renamed
    VILLAGE = "village"
    STREET = "street"

    TYPE_CHOICES = [
        (VILLAGE, "Village"),
        (STREET, "Street"),
    ]
    
    name = models.CharField(max_length=100)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE,related_name="villages_streets")

    type = models.CharField(
        blank=True,null=True,
        max_length=10,
        choices=TYPE_CHOICES
    )
    
    def __str__(self):
        return f"{self.name}, {self.ward.name}"



class Hamlet(AuditModel):
    name = models.CharField(max_length=100)
    village_street = models.ForeignKey(VillageStreet, on_delete=models.CASCADE,related_name="hamlets")

    def __str__(self):
        return f"{self.name}, {self.village.name}"
