# 24068022 Soh Kai Xuan
from django.db import models
from django.conf import settings
from disasters.models import AidRequest
from shelters.models import Shelter

User = settings.AUTH_USER_MODEL

class VolunteerAssignment(models.Model):
    """
    Model for assigning volunteers to specific tasks
    """
    STATUS_CHOICES = [
        ('ASSIGNED', 'Assigned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
    ]
    
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    aid_request = models.ForeignKey(AidRequest, on_delete=models.CASCADE, related_name='volunteer_assignments', null=True, blank=True)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='volunteer_assignments', null=True, blank=True)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_assignments')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ASSIGNED')
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.volunteer.username} - {self.title} ({self.get_status_display()})"


class VolunteerAvailability(models.Model):
    """
    Model for tracking volunteer availability
    """
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability_records')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.volunteer.username} - {'Available' if self.is_available else 'Unavailable'} ({self.start_date} to {self.end_date})"
