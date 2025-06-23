# 24068022 Soh Kai Xuan
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Shelter(models.Model):
    """
    Model for emergency shelters
    """
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    total_capacity = models.PositiveIntegerField(default=0)
    current_occupancy = models.PositiveIntegerField(default=0)
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    amenities = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    managed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_shelters')
    
    @property
    def available_capacity(self):
        return max(0, self.total_capacity - self.current_occupancy)
    
    @property
    def is_full(self):
        return self.current_occupancy >= self.total_capacity
    
    def __str__(self):
        return f"{self.name} - {self.available_capacity}/{self.total_capacity} available"


class ShelterRegistration(models.Model):
    """
    Model for tracking people registered at shelters
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('CHECKED_OUT', 'Checked Out'),
    ]
    
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='registrations')
    citizen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shelter_stays')
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    special_needs = models.TextField(blank=True)
    family_size = models.PositiveIntegerField(default=1)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='shelter_registrations')
    
    def __str__(self):
        return f"{self.citizen.username} at {self.shelter.name} - {self.get_status_display()}"
