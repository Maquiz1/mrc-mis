from django import forms
from .models import Household

class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ['household_head_name', 'number_of_men', 'number_of_women', 'household_head_phone_number', 'village_street']
        widgets = {
            'number_of_men': forms.NumberInput(attrs={'min': 0, 'step': 1, 'class': 'form-control'}),
            'number_of_women': forms.NumberInput(attrs={'min': 0, 'step': 1, 'class': 'form-control'}),
            'household_head_name': forms.TextInput(attrs={'class': 'form-control'}),
            'household_head_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'village_street': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class HouseholdUploadForm(forms.Form):
    file = forms.FileField(
        label="Upload Household Data (Excel or CSV)",
        help_text="Accepted formats: .xlsx, .csv"
    )
