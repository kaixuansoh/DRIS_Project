# 24068022 Soh Kai Xuan
from django import forms
from .models import DisasterReport, AidRequest

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

class AidRequestForm(forms.ModelForm):
    """
    Form for citizens to submit aid requests during disasters
    """
    class Meta:
        model = AidRequest
        fields = [
            'aid_type',
            'disaster_report',
            'description',
            'priority',
            'people_count',
        ]
        widgets = {
            'aid_type': forms.Select(attrs={'class': 'form-control'}),
            'disaster_report': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'people_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        help_texts = {
            'aid_type': 'Select the type of aid you need',
            'description': 'Provide details about your situation and what you need',
            'people_count': 'How many people need this aid?',
        }

class AidRequestManagementForm(forms.ModelForm):
    """
    Form for authorities to manage aid requests
    """
    class Meta:
        model = AidRequest
        fields = ['status', 'approved_by', 'completed_at']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'approved_by': forms.HiddenInput(),
            'completed_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
