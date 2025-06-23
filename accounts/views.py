# 24068022 Soh Kai Xuan
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import (
    CitizenSignUpForm, VolunteerSignUpForm, AuthoritySignUpForm, UserLoginForm,
    UserUpdateForm, CitizenProfileUpdateForm, VolunteerProfileUpdateForm, AuthorityProfileUpdateForm
)
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'


class SignUpView(TemplateView):
    template_name = 'accounts/signup_choice.html'


class CitizenSignUpView(CreateView):
    model = User
    form_class = CitizenSignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Citizen'
        return super().get_context_data(**kwargs)


class VolunteerSignUpView(CreateView):
    model = User
    form_class = VolunteerSignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Volunteer'
        return super().get_context_data(**kwargs)


class AuthoritySignUpView(CreateView):
    model = User
    form_class = AuthoritySignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Authority'
        return super().get_context_data(**kwargs)


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def update_profile(request):
    user_form = UserUpdateForm(instance=request.user)
    
    # Initialize the appropriate profile form based on user type
    profile_form = None
    if request.user.is_citizen():
        profile_form = CitizenProfileUpdateForm(instance=request.user.citizen_profile)
        template = 'accounts/update_citizen_profile.html'
    elif request.user.is_volunteer():
        profile_form = VolunteerProfileUpdateForm(instance=request.user.volunteer_profile)
        template = 'accounts/update_volunteer_profile.html'
    elif request.user.is_authority():
        profile_form = AuthorityProfileUpdateForm(instance=request.user.authority_profile)
        template = 'accounts/update_authority_profile.html'
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        
        # Process the appropriate profile form
        if request.user.is_citizen():
            profile_form = CitizenProfileUpdateForm(request.POST, instance=request.user.citizen_profile)
        elif request.user.is_volunteer():
            profile_form = VolunteerProfileUpdateForm(request.POST, instance=request.user.volunteer_profile)
        elif request.user.is_authority():
            profile_form = AuthorityProfileUpdateForm(request.POST, instance=request.user.authority_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, template, context)
