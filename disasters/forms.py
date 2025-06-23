# 24068022 Soh Kai Xuan
from django import forms
from .models import DisasterReport

class DisasterReportForm(forms.ModelForm):
    """
    Form for citizens to submit disaster reports
    """
    class Meta:
        model = DisasterReport
        fields = [
            'disaster_type',
            'location',
            'description',
            'severity',
            'latitude',
            'longitude',
        ]
        widgets = {
            'disaster_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Optional: e.g. 3.140853',
                'step': 'any'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Optional: e.g. 101.693207',
                'step': 'any'
            }),
        }
        help_texts = {
            'location': 'Enter a descriptive location (e.g., street address, landmark)',
            'latitude': 'Optional: You can provide precise coordinates if known',
            'longitude': 'Optional: You can provide precise coordinates if known',
        }
