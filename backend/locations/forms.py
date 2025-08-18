from django import forms
from .models import Country, Region, District, Site, Ward, VillageStreet, Hamlet

# ------------------ Country ------------------
class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ------------------ Region ------------------        
class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'country']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter region name'
            }),
            'country': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'name': 'Region Name',
            'country': 'Country',
        }

# ------------------ District ------------------
class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['name', 'region']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
        }

# ------------------ Site ------------------
class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['name', 'district']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-select'}),
        }

# ------------------ Ward ------------------
class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = ['name', 'district']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-select'}),
        }

# ------------------ Village ------------------
class VillageStreetForm(forms.ModelForm):  # Renamed
    class Meta:
        model = VillageStreet
        fields = ['name', 'ward']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ward': forms.Select(attrs={'class': 'form-select'}),
        }


# ------------------ Hamlet ------------------
class HamletForm(forms.ModelForm):
    class Meta:
        model = Hamlet
        fields = ['name', 'village']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'village': forms.Select(attrs={'class': 'form-select'}),
        }
