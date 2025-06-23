# 24068022 Soh Kai Xuan
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from .models import DisasterReport
from .forms import DisasterReportForm
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
