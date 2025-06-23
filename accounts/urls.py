# 24068022 Soh Kai Xuan
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from . import admin_views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/citizen/', views.CitizenSignUpView.as_view(), name='citizen_signup'),
    path('signup/volunteer/', views.VolunteerSignUpView.as_view(), name='volunteer_signup'),
    path('signup/authority/', views.AuthoritySignUpView.as_view(), name='authority_signup'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    
    # User management routes
    path('manage/', admin_views.manage_users, name='manage_users'),
    path('user/<int:user_id>/', admin_views.user_detail, name='user_detail'),
    path('user/<int:user_id>/toggle-status/', admin_views.toggle_user_status, name='toggle_user_status'),
    path('user/<int:user_id>/toggle-staff/', admin_views.toggle_staff_status, name='toggle_staff_status'),
]
