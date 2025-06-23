# 24068022 Soh Kai Xuan
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/citizen/', views.CitizenSignUpView.as_view(), name='citizen_signup'),
    path('signup/volunteer/', views.VolunteerSignUpView.as_view(), name='volunteer_signup'),
    path('signup/authority/', views.AuthoritySignUpView.as_view(), name='authority_signup'),
    path('profile/', views.profile_view, name='profile'),
]
