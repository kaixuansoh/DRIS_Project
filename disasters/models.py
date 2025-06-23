# 24068022 Soh Kai Xuan
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class DisasterReport(models.Model):
    """
    Model for citizen disaster reports, containing information about disaster events
    """
    DISASTER_TYPE_CHOICES = [
        ('FLOOD', 'Flood'),
        ('FIRE', 'Fire'),
        ('EARTHQUAKE', 'Earthquake'),
        ('LANDSLIDE', 'Landslide'),
        ('HURRICANE', 'Hurricane'),
        ('TSUNAMI', 'Tsunami'),
        ('OTHER', 'Other'),
    ]
    
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disaster_reports')
    disaster_type = models.CharField(max_length=20, choices=DISASTER_TYPE_CHOICES)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='MEDIUM')
    reported_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_reports')
    
    def __str__(self):
        return f"{self.get_disaster_type_display()} at {self.location} ({self.reported_at})"


class AidRequest(models.Model):
    """
    Model for citizens to request aid during disasters
    """
    AID_TYPE_CHOICES = [
        ('FOOD', 'Food'),
        ('WATER', 'Water'),
        ('SHELTER', 'Shelter'),
        ('MEDICAL', 'Medical'),
        ('RESCUE', 'Rescue'),
        ('EVACUATION', 'Evacuation'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('DENIED', 'Denied'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aid_requests')
    aid_type = models.CharField(max_length=20, choices=AID_TYPE_CHOICES)
    disaster_report = models.ForeignKey(DisasterReport, on_delete=models.CASCADE, related_name='aid_requests')
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')], default='MEDIUM')
    people_count = models.PositiveIntegerField(default=1, help_text="Number of people needing aid")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_aid_requests')
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_aid_type_display()} aid for {self.requester.username} - {self.get_status_display()}"
