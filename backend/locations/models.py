# locations/models.py

from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class Region(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class District(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.region.name}"


class Site(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.district.name}"


class Ward(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.district.name}"


class VillageStreet(models.Model):  # Renamed
    name = models.CharField(max_length=100)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.ward.name}"



class Hamlet(models.Model):
    name = models.CharField(max_length=100)
    village = models.ForeignKey(VillageStreet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.village.name}"
