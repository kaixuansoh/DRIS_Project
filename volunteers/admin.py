# 24068022 Soh Kai Xuan
from django.contrib import admin
from .models import VolunteerAssignment, VolunteerAvailability


@admin.register(VolunteerAssignment)
class VolunteerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'title', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'created_at', 'start_date')
    search_fields = ('volunteer__username', 'title', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Assignment Information', {
            'fields': ('volunteer', 'title', 'description', 'status')
        }),
        ('Related to', {
            'fields': ('aid_request', 'shelter')
        }),
        ('Timing', {
            'fields': ('created_at', 'start_date', 'end_date')
        }),
        ('Management', {
            'fields': ('assigned_by', 'notes')
        }),
    )
    list_per_page = 25


@admin.register(VolunteerAvailability)
class VolunteerAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'is_available', 'start_date', 'end_date')
    list_filter = ('is_available', 'start_date')
    search_fields = ('volunteer__username', 'notes')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Availability Information', {
            'fields': ('volunteer', 'is_available')
        }),
        ('Time Period', {
            'fields': ('start_date', 'end_date', 'created_at')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )
    list_per_page = 25
