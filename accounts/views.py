# 24068022 Soh Kai Xuan
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import CitizenSignUpForm, VolunteerSignUpForm, AuthoritySignUpForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from .models import User


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'


class SignUpView(TemplateView):
    template_name = 'accounts/signup_choice.html'


class CitizenSignUpView(CreateView):
    model = User
    form_class = CitizenSignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Citizen'
        return super().get_context_data(**kwargs)


class VolunteerSignUpView(CreateView):
    model = User
    form_class = VolunteerSignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Volunteer'
        return super().get_context_data(**kwargs)


class AuthoritySignUpView(CreateView):
    model = User
    form_class = AuthoritySignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Authority'
        return super().get_context_data(**kwargs)


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
