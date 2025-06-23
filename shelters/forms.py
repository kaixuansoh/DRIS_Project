# 24068022 Soh Kai Xuan
from django import forms
from .models import Shelter

class ShelterForm(forms.ModelForm):
    """
    Form for creating and updating shelters
    """
    class Meta:
        model = Shelter
        fields = [
            'name',
            'address',
            'total_capacity',
            'current_occupancy',
            'contact_person',
            'contact_phone',
            'is_active',
            'amenities',
            'managed_by',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'total_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_occupancy': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'amenities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'managed_by': forms.Select(attrs={'class': 'form-control'}),
        }
