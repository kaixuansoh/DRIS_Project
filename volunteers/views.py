# 24068022 Soh Kai Xuan
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone

from .models import VolunteerAvailability, VolunteerAssignment
from .forms import VolunteerAvailabilityForm, VolunteerAssignmentForm

# Volunteer Availability Views
@login_required
def availability_list(request):
    """View for volunteers to see their availability records"""
    if not request.user.is_volunteer():
        return HttpResponseForbidden("You must be a volunteer to access this page.")
    
    availability_list = VolunteerAvailability.objects.filter(
        volunteer=request.user
    ).order_by('-start_date')
    
    return render(request, 'volunteers/availability_list.html', {
        'availability_list': availability_list
    })

@login_required
def update_availability(request):
    """View for volunteers to update their availability"""
    if not request.user.is_volunteer():
        return HttpResponseForbidden("You must be a volunteer to access this page.")
    
    if request.method == 'POST':
        form = VolunteerAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.volunteer = request.user
            availability.save()
            messages.success(request, "Your availability has been updated successfully.")
            return redirect('volunteers:availability_list')
    else:
        form = VolunteerAvailabilityForm()
    
    return render(request, 'volunteers/update_availability.html', {
        'form': form
    })

@login_required
def edit_availability(request, availability_id):
    """View for volunteers to edit an existing availability record"""
    if not request.user.is_volunteer():
        return HttpResponseForbidden("You must be a volunteer to access this page.")
    
    availability = get_object_or_404(VolunteerAvailability, id=availability_id, volunteer=request.user)
    
    if request.method == 'POST':
        form = VolunteerAvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            messages.success(request, "Your availability has been updated successfully.")
            return redirect('volunteers:availability_list')
    else:
        form = VolunteerAvailabilityForm(instance=availability)
    
    return render(request, 'volunteers/update_availability.html', {
        'form': form,
        'edit_mode': True
    })

@login_required
def delete_availability(request, availability_id):
    """View for volunteers to delete an availability record"""
    if not request.user.is_volunteer():
        return HttpResponseForbidden("You must be a volunteer to access this page.")
    
    availability = get_object_or_404(VolunteerAvailability, id=availability_id, volunteer=request.user)
    availability.delete()
    messages.success(request, "Availability record has been deleted.")
    return redirect('volunteers:availability_list')

# Volunteer Assignment Views
@login_required
def assignment_list(request):
    """View for volunteers to see their assignments"""
    if not request.user.is_volunteer():
        return HttpResponseForbidden("You must be a volunteer to access this page.")
    
    assignments = VolunteerAssignment.objects.filter(volunteer=request.user).order_by('-start_date')
    
    return render(request, 'volunteers/assignment_list.html', {
        'assignments': assignments
    })

@login_required
def update_assignment_status(request, assignment_id, new_status):
    """View for volunteers to update the status of their assignments"""
    if not request.user.is_volunteer():
        return HttpResponseForbidden("You must be a volunteer to access this page.")
    
    valid_transitions = {
        'ASSIGNED': ['IN_PROGRESS'],
        'IN_PROGRESS': ['COMPLETED']
    }
    
    assignment = get_object_or_404(VolunteerAssignment, id=assignment_id, volunteer=request.user)
    
    if new_status in valid_transitions.get(assignment.status, []):
        assignment.status = new_status
        if new_status == 'IN_PROGRESS':
            assignment.volunteer_start_date = timezone.now()
        elif new_status == 'COMPLETED':
            assignment.volunteer_complete_date = timezone.now()
        assignment.save()
        
        status_display = dict(VolunteerAssignment.STATUS_CHOICES)[new_status]
        messages.success(request, f"Assignment status updated to {status_display}.")
    else:
        messages.error(request, "Invalid status transition.")
    
    return redirect('volunteers:assignment_list')

# Authority Assignment Management Views
@login_required
def manage_assignments(request):
    """View for authorities to manage all assignments"""
    if not request.user.is_authority():
        return HttpResponseForbidden("You must be an authority to access this page.")
    
    assignments = VolunteerAssignment.objects.all().order_by('-created_at')
    
    return render(request, 'volunteers/manage_assignments.html', {
        'assignments': assignments
    })

@login_required
def create_assignment(request):
    """View for authorities to create new assignments"""
    if not request.user.is_authority():
        return HttpResponseForbidden("You must be an authority to access this page.")
    
    if request.method == 'POST':
        form = VolunteerAssignmentForm(request.POST, user=request.user)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.assigned_by = request.user
            assignment.save()
            messages.success(request, "Volunteer assignment created successfully.")
            return redirect('volunteers:manage_assignments')
    else:
        form = VolunteerAssignmentForm(user=request.user)
    
    return render(request, 'volunteers/create_assignment.html', {
        'form': form
    })

@login_required
def edit_assignment(request, assignment_id):
    """View for authorities to edit assignments"""
    if not request.user.is_authority():
        return HttpResponseForbidden("You must be an authority to access this page.")
    
    assignment = get_object_or_404(VolunteerAssignment, id=assignment_id)
    
    if request.method == 'POST':
        form = VolunteerAssignmentForm(request.POST, instance=assignment, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment updated successfully.")
            return redirect('volunteers:manage_assignments')
    else:
        form = VolunteerAssignmentForm(instance=assignment, user=request.user)
    
    return render(request, 'volunteers/create_assignment.html', {
        'form': form,
        'edit_mode': True
    })

@login_required
def cancel_assignment(request, assignment_id):
    """View for authorities to cancel assignments"""
    if not request.user.is_authority():
        return HttpResponseForbidden("You must be an authority to access this page.")
    
    assignment = get_object_or_404(VolunteerAssignment, id=assignment_id)
    if assignment.status not in ['COMPLETED', 'CANCELED']:
        assignment.status = 'CANCELED'
        assignment.save()
        messages.success(request, "Assignment has been canceled.")
    else:
        messages.error(request, "Cannot cancel a completed or already canceled assignment.")
    
    return redirect('volunteers:manage_assignments')
