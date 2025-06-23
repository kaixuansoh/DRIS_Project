# 24068022 Soh Kai Xuan
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, CitizenProfile, VolunteerProfile, AuthorityProfile


class UserLoginForm(AuthenticationForm):
    """
    Form for user login
    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class CitizenSignUpForm(UserCreationForm):
    """
    Form for citizen registration
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number'
    }))
    address = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Address',
        'rows': 3
    }))
    emergency_contact = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Emergency Contact Number'
    }))
    medical_conditions = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Any Medical Conditions (optional)',
        'rows': 3
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'CITIZEN'
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.address = self.cleaned_data['address']
        
        if commit:
            user.save()
            citizen_profile = CitizenProfile(
                user=user,
                emergency_contact=self.cleaned_data['emergency_contact'],
                medical_conditions=self.cleaned_data['medical_conditions']
            )
            citizen_profile.save()
        
        return user


class VolunteerSignUpForm(UserCreationForm):
    """
    Form for volunteer registration
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number'
    }))
    address = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Address',
        'rows': 3
    }))
    skills = forms.ChoiceField(choices=VolunteerProfile.SKILL_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    certifications = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Certifications (if any)',
        'rows': 3
    }))
    experience = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Relevant Experience',
        'rows': 3
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'VOLUNTEER'
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.address = self.cleaned_data['address']
        
        if commit:
            user.save()
            volunteer_profile = VolunteerProfile(
                user=user,
                skills=self.cleaned_data['skills'],
                certifications=self.cleaned_data['certifications'],
                experience=self.cleaned_data['experience']
            )
            volunteer_profile.save()
        
        return user


class AuthoritySignUpForm(UserCreationForm):
    """
    Form for authority registration
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number'
    }))
    department = forms.ChoiceField(choices=AuthorityProfile.DEPARTMENT_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    position = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Position/Title'
    }))
    badge_number = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Badge/ID Number'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'AUTHORITY'
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        
        if commit:
            user.save()
            authority_profile = AuthorityProfile(
                user=user,
                department=self.cleaned_data['department'],
                position=self.cleaned_data['position'],
                badge_number=self.cleaned_data['badge_number']
            )
            authority_profile.save()
        
        return user

# Profile Update Forms
class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic user information
    """
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number'
    }))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Address',
        'rows': 3
    }))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address')


class CitizenProfileUpdateForm(forms.ModelForm):
    """
    Form for updating citizen profile information
    """
    emergency_contact = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Emergency Contact Number'
    }))
    medical_conditions = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Any Medical Conditions',
        'rows': 3
    }))
    
    class Meta:
        model = CitizenProfile
        fields = ('emergency_contact', 'medical_conditions')


class VolunteerProfileUpdateForm(forms.ModelForm):
    """
    Form for updating volunteer profile information
    """
    skills = forms.ChoiceField(choices=VolunteerProfile.SKILL_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    availability = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))
    certifications = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Certifications',
        'rows': 3
    }))
    experience = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Relevant Experience',
        'rows': 3
    }))
    
    class Meta:
        model = VolunteerProfile
        fields = ('skills', 'availability', 'certifications', 'experience')


class AuthorityProfileUpdateForm(forms.ModelForm):
    """
    Form for updating authority profile information
    """
    department = forms.ChoiceField(choices=AuthorityProfile.DEPARTMENT_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    position = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Position/Title'
    }))
    badge_number = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Badge/ID Number'
    }))
    
    class Meta:
        model = AuthorityProfile
        fields = ('department', 'position', 'badge_number')
