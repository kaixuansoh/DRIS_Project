# 24068022 Soh Kai Xuan
from django.contrib import admin
from .models import Shelter, ShelterRegistration


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'total_capacity', 'current_occupancy', 'is_active', 'managed_by')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'address', 'contact_person', 'contact_phone')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Shelter Information', {
            'fields': ('name', 'address', 'total_capacity', 'current_occupancy', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_phone')
        }),
        ('Management', {
            'fields': ('managed_by', 'amenities')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    list_per_page = 25


@admin.register(ShelterRegistration)
class ShelterRegistrationAdmin(admin.ModelAdmin):
    list_display = ('shelter', 'citizen', 'status', 'check_in_time', 'family_size')
    list_filter = ('status', 'check_in_time', 'shelter')
    search_fields = ('citizen__username', 'special_needs')
    readonly_fields = ('check_in_time',)
    fieldsets = (
        ('Registration Information', {
            'fields': ('shelter', 'citizen', 'status', 'family_size')
        }),
        ('Timing', {
            'fields': ('check_in_time', 'check_out_time')
        }),
        ('Additional Information', {
            'fields': ('special_needs', 'registered_by')
        }),
    )
    list_per_page = 25
