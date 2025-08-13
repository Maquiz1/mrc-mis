from django import forms
from .models import Household

class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ['household_head_name', 'number_of_men', 'number_of_women', 'household_head_phone_number', 'village_street']
        widgets = {
            'household_head_name': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_men': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_women': forms.NumberInput(attrs={'class': 'form-control'}),
            'household_head_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'village_street': forms.TextInput(attrs={'class': 'form-control'}),
        }
