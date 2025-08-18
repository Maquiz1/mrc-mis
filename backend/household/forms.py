# households/forms.py
from django import forms
from .models import Household,HamletHouseholdExpectation
from locations.models import Region, District, Ward, VillageStreet, Hamlet
import pandas as pd


class HamletHouseholdExpectationUploadForm(forms.Form):
    file = forms.FileField(
        label="Select Excel or CSV file",
        help_text="Max. 10MB"
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        if not (file.name.endswith('.csv') or file.name.endswith('.xlsx')):
            raise forms.ValidationError("File must be CSV or Excel.")
        return file

    def save(self):
        file = self.cleaned_data['file']
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        for _, row in df.iterrows():
            # Match Hamlet by name
            hamlet_name = row.get('hamlet', '')
            expected = row.get('expected_households', 0)
            hamlet = Hamlet.objects.filter(name=hamlet_name).first()
            if hamlet:
                HamletHouseholdExpectation.objects.update_or_create(
                    hamlet=hamlet,
                    defaults={'expected_households': expected}
                )

class HamletHouseholdExpectationForm(forms.ModelForm):
    class Meta:
        model = HamletHouseholdExpectation
        fields = ['hamlet', 'expected_households']
        
class HouseholdForm(forms.ModelForm):
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    district = forms.ModelChoiceField(
        queryset=District.objects.none(),  # will be filtered dynamically via JS
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    ward = forms.ModelChoiceField(
        queryset=Ward.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    village_street = forms.ModelChoiceField(
        queryset=VillageStreet.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    hamlet = forms.ModelChoiceField(
        queryset=Hamlet.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Household
        fields = [
            'household_head_name', 
            'number_of_men', 
            'number_of_women', 
            'household_head_phone_number',
            'region', 
            'district', 
            'ward', 
            'village_street',
            'hamlet'
        ]
        widgets = {
            'number_of_men': forms.NumberInput(attrs={'min': 0, 'step': 1, 'class': 'form-control'}),
            'number_of_women': forms.NumberInput(attrs={'min': 0, 'step': 1, 'class': 'form-control'}),
            'household_head_name': forms.TextInput(attrs={'class': 'form-control'}),
            'household_head_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class HouseholdUploadForm(forms.Form):
    file = forms.FileField(
        label="Upload Household Data (Excel or CSV)",
        help_text="Accepted formats: .xlsx, .csv"
    )
