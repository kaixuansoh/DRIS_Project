# 24068022 Soh Kai Xuan
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from .models import DisasterReport, AidRequest
from .forms import DisasterReportForm, AidRequestForm, AidRequestManagementForm
from django.utils import timezone

# Helper function to check if user is admin/authority
def is_admin_or_authority(user):
    return user.is_authenticated and (user.is_staff or hasattr(user, 'is_authority') and user.is_authority())

# Create your views here.
@login_required
def submit_disaster_report(request):
    """
    View to allow citizens to submit a new disaster report
    """
    if request.method == 'POST':
        form = DisasterReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            messages.success(request, 'Your disaster report has been submitted successfully!')
            return redirect('disasters:my_reports')
    else:
        form = DisasterReportForm()
    
    context = {
        'form': form,
        'title': 'Submit Disaster Report'
    }
    return render(request, 'disasters/submit_report.html', context)

@login_required
def my_reports(request):
    """
    View to display a list of disaster reports submitted by the current user
    """
    reports = DisasterReport.objects.filter(reporter=request.user).order_by('-reported_at')
    context = {
        'reports': reports,
        'title': 'My Disaster Reports'
    }
    return render(request, 'disasters/my_reports.html', context)

@login_required
def report_detail(request, report_id):
    """
    View to display detailed information about a specific disaster report
    """
    report = get_object_or_404(DisasterReport, id=report_id)
    # Check if the user is the owner or an authority
    if request.user != report.reporter and not hasattr(request.user, 'is_authority') and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this report.")
        return redirect('disasters:my_reports')
    
    context = {
        'report': report,
        'title': f'Disaster Report: {report.get_disaster_type_display()}'
    }
    return render(request, 'disasters/report_detail.html', context)

# Admin management views
@login_required
@user_passes_test(is_admin_or_authority)
def manage_reports(request):
    """
    Admin view to list and manage all disaster reports
    """
    # Get query parameters for filtering
    disaster_type = request.GET.get('disaster_type', '')
    severity = request.GET.get('severity', '')
    verified = request.GET.get('verified', '')
    
    reports = DisasterReport.objects.all().order_by('-reported_at')
    
    # Apply filters if provided
    if disaster_type:
        reports = reports.filter(disaster_type=disaster_type)
    if severity:
        reports = reports.filter(severity=severity)
    if verified:
        is_verified = verified == 'yes'
        reports = reports.filter(is_verified=is_verified)
    
    context = {
        'reports': reports,
        'title': 'Manage Disaster Reports',
        'disaster_types': DisasterReport.DISASTER_TYPE_CHOICES,
        'severity_levels': DisasterReport.SEVERITY_CHOICES,
        'current_filters': {
            'disaster_type': disaster_type,
            'severity': severity,
            'verified': verified
        }
    }
    return render(request, 'disasters/manage_reports.html', context)

@login_required
@user_passes_test(is_admin_or_authority)
def verify_report(request, report_id):
    """
    Admin view to verify a disaster report
    """
    report = get_object_or_404(DisasterReport, id=report_id)
    
    # Toggle verification status
    report.is_verified = not report.is_verified
    
    if report.is_verified:
        report.verified_by = request.user
    else:
        report.verified_by = None
        
    report.save()
    
    action = "verified" if report.is_verified else "unverified"
    messages.success(request, f"Report has been {action} successfully.")
    
    # Redirect back to the referring page or manage reports page
    next_page = request.GET.get('next', reverse('disasters:manage_reports'))
    return redirect(next_page)

@login_required
@user_passes_test(is_admin_or_authority)
def delete_report(request, report_id):
    """
    Admin view to delete a disaster report
    """
    report = get_object_or_404(DisasterReport, id=report_id)
    
    if request.method == 'POST':
        report_type = report.get_disaster_type_display()
        report.delete()
        messages.success(request, f"The {report_type} report at {report.location} has been deleted successfully.")
        return redirect('disasters:manage_reports')
        
    context = {
        'report': report,
        'title': 'Delete Disaster Report'
    }
    return render(request, 'disasters/delete_report.html', context)

# Aid Request Views
@login_required
def submit_aid_request(request):
    """
    View for citizens to submit a new aid request
    """
    # Only show disasters that are verified or reported by the current user
    available_reports = DisasterReport.objects.filter(
        is_verified=True
    ).order_by('-reported_at')
    
    # Also include reports submitted by the current user
    user_reports = DisasterReport.objects.filter(reporter=request.user)
    available_reports = (available_reports | user_reports).distinct()
    
    if request.method == 'POST':
        form = AidRequestForm(request.POST)
        if form.is_valid():
            aid_request = form.save(commit=False)
            aid_request.requester = request.user
            aid_request.save()
            messages.success(request, 'Your aid request has been submitted successfully!')
            return redirect('disasters:my_aid_requests')
    else:
        initial_report_id = request.GET.get('report_id')
        initial_data = {}
        if initial_report_id:
            try:
                report = DisasterReport.objects.get(id=initial_report_id)
                if report.is_verified or report.reporter == request.user:
                    initial_data['disaster_report'] = report
            except DisasterReport.DoesNotExist:
                pass
        
        form = AidRequestForm(initial=initial_data)
        form.fields['disaster_report'].queryset = available_reports
    
    context = {
        'form': form,
        'title': 'Request Aid'
    }
    return render(request, 'disasters/submit_aid_request.html', context)

@login_required
def my_aid_requests(request):
    """
    View for citizens to see their aid requests
    """
    aid_requests = AidRequest.objects.filter(requester=request.user).order_by('-requested_at')
    context = {
        'aid_requests': aid_requests,
        'title': 'My Aid Requests'
    }
    return render(request, 'disasters/my_aid_requests.html', context)

@login_required
def aid_request_detail(request, request_id):
    """
    View to display detailed information about a specific aid request
    """
    aid_request = get_object_or_404(AidRequest, id=request_id)
    # Check if the user is the owner or an authority
    if request.user != aid_request.requester and not is_admin_or_authority(request.user):
        messages.error(request, "You don't have permission to view this aid request.")
        return redirect('disasters:my_aid_requests')
    
    context = {
        'aid_request': aid_request,
        'title': f'Aid Request: {aid_request.get_aid_type_display()}'
    }
    return render(request, 'disasters/aid_request_detail.html', context)

@login_required
@user_passes_test(is_admin_or_authority)
def manage_aid_requests(request):
    """
    Admin view to list and manage all aid requests
    """
    # Get query parameters for filtering
    aid_type = request.GET.get('aid_type', '')
    priority = request.GET.get('priority', '')
    status = request.GET.get('status', '')
    
    aid_requests = AidRequest.objects.all().order_by('-requested_at')
    
    # Apply filters if provided
    if aid_type:
        aid_requests = aid_requests.filter(aid_type=aid_type)
    if priority:
        aid_requests = aid_requests.filter(priority=priority)
    if status:
        aid_requests = aid_requests.filter(status=status)
    
    context = {
        'aid_requests': aid_requests,
        'title': 'Manage Aid Requests',
        'aid_types': AidRequest.AID_TYPE_CHOICES,
        'priority_levels': [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')],
        'statuses': AidRequest.STATUS_CHOICES,
        'current_filters': {
            'aid_type': aid_type,
            'priority': priority,
            'status': status
        }
    }
    return render(request, 'disasters/manage_aid_requests.html', context)

@login_required
@user_passes_test(is_admin_or_authority)
def update_aid_request(request, request_id):
    """
    Admin view to update the status of an aid request
    """
    aid_request = get_object_or_404(AidRequest, id=request_id)
    
    if request.method == 'POST':
        form = AidRequestManagementForm(request.POST, instance=aid_request)
        if form.is_valid():
            updated_request = form.save(commit=False)
            
            # Handle status changes
            if updated_request.status == 'APPROVED' and aid_request.status != 'APPROVED':
                updated_request.approved_by = request.user
            
            # If status is completed and wasn't before, set completed_at
            if updated_request.status == 'COMPLETED' and aid_request.status != 'COMPLETED':
                updated_request.completed_at = timezone.now()
            
            # If status changed from completed to something else, clear completed_at
            if updated_request.status != 'COMPLETED' and aid_request.status == 'COMPLETED':
                updated_request.completed_at = None
                
            updated_request.save()
            messages.success(request, f'Aid request status updated to {updated_request.get_status_display()}')
            return redirect('disasters:manage_aid_requests')
    else:
        initial_data = {'approved_by': request.user}
        form = AidRequestManagementForm(instance=aid_request, initial=initial_data)
    
    context = {
        'form': form,
        'aid_request': aid_request,
        'title': f'Update Aid Request: {aid_request.get_aid_type_display()}'
    }
    return render(request, 'disasters/update_aid_request.html', context)
