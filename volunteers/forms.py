# 24068022 Soh Kai Xuan
from django import forms
from .models import VolunteerAvailability, VolunteerAssignment
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class VolunteerAvailabilityForm(forms.ModelForm):
    """Form for volunteers to update their availability"""
    
    class Meta:
        model = VolunteerAvailability
        fields = ['start_date', 'end_date', 'is_available', 'notes']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control volunteer-form'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control volunteer-form'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input volunteer-form'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control volunteer-form'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        # Validate that start_date is before end_date
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        # Validate that start_date is not in the past
        from django.utils import timezone
        if start_date and start_date < timezone.now():
            raise forms.ValidationError("Start date cannot be in the past.")
            
        return cleaned_data


class VolunteerAssignmentForm(forms.ModelForm):
    """Form for authorities to assign tasks to volunteers"""
    volunteer = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type='VOLUNTEER'),
        empty_label="Select a volunteer",
    )
    
    class Meta:
        model = VolunteerAssignment
        fields = ['volunteer', 'title', 'description', 'status', 
                 'start_date', 'end_date', 'notes', 'aid_request', 'shelter']
        widgets = {
            'volunteer': forms.Select(attrs={'class': 'form-select volunteer-form'}),
            'title': forms.TextInput(attrs={'class': 'form-control volunteer-form'}),
            'status': forms.Select(attrs={'class': 'form-select volunteer-form'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control volunteer-form'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control volunteer-form'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control volunteer-form'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control volunteer-form'}),
            'aid_request': forms.Select(attrs={'class': 'form-select volunteer-form'}),
            'shelter': forms.Select(attrs={'class': 'form-select volunteer-form'}),
        }
        
    def __init__(self, *args, **kwargs):
        # Get available volunteers
        self.user = kwargs.pop('user', None)
        super(VolunteerAssignmentForm, self).__init__(*args, **kwargs)
        
        # Filter volunteers based on availability
        if 'volunteer' in self.fields:
            available_volunteers = self._get_available_volunteers()
            self.fields['volunteer'].queryset = User.objects.filter(
                id__in=available_volunteers,
                user_type='VOLUNTEER'
            )
    
    def _get_available_volunteers(self):
        """Get volunteers who are available based on VolunteerAvailability records"""
        current_time = timezone.now()
        # Find volunteers with active availability records
        available_volunteers = VolunteerAvailability.objects.filter(
            is_available=True,
            start_date__lte=current_time,
            end_date__gte=current_time
        ).values_list('volunteer', flat=True).distinct()
        
        # If there are no specific availability records, return all volunteer users
        if not available_volunteers:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            available_volunteers = User.objects.filter(user_type='VOLUNTEER').values_list('id', flat=True)
        
        return available_volunteers

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date.")
            
        return cleaned_data
