# 24068022 Soh Kai Xuan
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import User, CitizenProfile, VolunteerProfile, AuthorityProfile
from django.core.paginator import Paginator
from django.db.models import Q


def is_admin_or_staff(user):
    """Check if the user is an admin or staff member"""
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_admin_or_staff)
def manage_users(request):
    """View for administrators to manage all user accounts"""
    # Get filter parameters
    user_type = request.GET.get('user_type', '')
    search_query = request.GET.get('search', '')
    
    # Start with all users
    users = User.objects.all().order_by('username')
    
    # Apply filters
    if user_type:
        users = users.filter(user_type=user_type)
        
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) | 
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) | 
            Q(email__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(users, 10)  # 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'user_type': user_type,
        'search_query': search_query,
        'user_types': User.USER_TYPE_CHOICES,
    }
    
    return render(request, 'accounts/manage_users.html', context)


@login_required
@user_passes_test(is_admin_or_staff)
def user_detail(request, user_id):
    """View detailed information for a single user"""
    user = get_object_or_404(User, id=user_id)
    
    # Get profile information based on user type
    profile = None
    if user.is_citizen():
        try:
            profile = CitizenProfile.objects.get(user=user)
        except CitizenProfile.DoesNotExist:
            profile = None
    elif user.is_volunteer():
        try:
            profile = VolunteerProfile.objects.get(user=user)
        except VolunteerProfile.DoesNotExist:
            profile = None
    elif user.is_authority():
        try:
            profile = AuthorityProfile.objects.get(user=user)
        except AuthorityProfile.DoesNotExist:
            profile = None
    
    context = {
        'user_detail': user,
        'profile': profile,
    }
    
    return render(request, 'accounts/user_detail.html', context)


@login_required
@user_passes_test(is_admin_or_staff)
def toggle_user_status(request, user_id):
    """Toggle a user's active status"""
    user = get_object_or_404(User, id=user_id)
    
    # Can't deactivate your own account
    if request.user == user:
        messages.error(request, "You cannot deactivate your own account.")
        return redirect('accounts:user_detail', user_id=user_id)
    
    user.is_active = not user.is_active
    user.save()
    
    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f"User account has been {status}.")
    
    return redirect('accounts:user_detail', user_id=user_id)


@login_required
@user_passes_test(is_admin_or_staff)
def toggle_staff_status(request, user_id):
    """Toggle a user's staff status"""
    user = get_object_or_404(User, id=user_id)
    
    # Can't remove your own staff status
    if request.user == user:
        messages.error(request, "You cannot change your own staff status.")
        return redirect('accounts:user_detail', user_id=user_id)
    
    user.is_staff = not user.is_staff
    user.save()
    
    status = "granted" if user.is_staff else "removed"
    messages.success(request, f"Staff status has been {status} for this user.")
    
    return redirect('accounts:user_detail', user_id=user_id)
