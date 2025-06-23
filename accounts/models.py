# 24068022 Soh Kai Xuan
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser to include role-based access control
    """
    USER_TYPE_CHOICES = [
        ('CITIZEN', 'Citizen'),
        ('VOLUNTEER', 'Volunteer'),
        ('AUTHORITY', 'Authority'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='CITIZEN')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    def is_citizen(self):
        return self.user_type == 'CITIZEN'
    
    def is_volunteer(self):
        return self.user_type == 'VOLUNTEER'
    
    def is_authority(self):
        return self.user_type == 'AUTHORITY'


class CitizenProfile(models.Model):
    """
    Additional information specific to citizens
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='citizen_profile')
    emergency_contact = models.CharField(max_length=15, blank=True)
    medical_conditions = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Citizen Profile"


class VolunteerProfile(models.Model):
    """
    Additional information specific to volunteers
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='volunteer_profile')
    
    SKILL_CHOICES = [
        ('MEDICAL', 'Medical'),
        ('RESCUE', 'Rescue'),
        ('LOGISTICS', 'Logistics'),
        ('COUNSELING', 'Counseling'),
        ('TECHNICAL', 'Technical'),
        ('OTHER', 'Other'),
    ]
    
    skills = models.CharField(max_length=20, choices=SKILL_CHOICES, default='OTHER')
    availability = models.BooleanField(default=True)
    certifications = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Volunteer Profile"


class AuthorityProfile(models.Model):
    """
    Additional information specific to authorities
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='authority_profile')
    
    DEPARTMENT_CHOICES = [
        ('POLICE', 'Police'),
        ('FIRE', 'Fire Department'),
        ('HEALTH', 'Health Department'),
        ('ADMIN', 'Administrative'),
        ('OTHER', 'Other'),
    ]
    
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='OTHER')
    position = models.CharField(max_length=100, blank=True)
    badge_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Authority Profile"
