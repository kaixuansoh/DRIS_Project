# 24068022 Soh Kai Xuan
from django.contrib import admin
from .models import User, CitizenProfile, VolunteerProfile, AuthorityProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'phone_number')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_per_page = 25


@admin.register(CitizenProfile)
class CitizenProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'emergency_contact')
    search_fields = ('user__username', 'emergency_contact', 'medical_conditions')
    list_filter = ('user__is_active',)


@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills', 'availability')
    list_filter = ('skills', 'availability')
    search_fields = ('user__username', 'certifications', 'experience')


@admin.register(AuthorityProfile)
class AuthorityProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position', 'badge_number')
    list_filter = ('department',)
    search_fields = ('user__username', 'position', 'badge_number')
