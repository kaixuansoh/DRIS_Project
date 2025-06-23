# 24068022 Soh Kai Xuan
from django.contrib import admin
from .models import DisasterReport, AidRequest


@admin.register(DisasterReport)
class DisasterReportAdmin(admin.ModelAdmin):
    list_display = ('disaster_type', 'location', 'severity', 'reported_at', 'is_verified', 'reporter')
    list_filter = ('disaster_type', 'severity', 'is_verified', 'reported_at')
    search_fields = ('location', 'description', 'reporter__username')
    readonly_fields = ('reported_at',)
    fieldsets = (
        ('Report Information', {
            'fields': ('reporter', 'disaster_type', 'severity', 'reported_at')
        }),
        ('Location Details', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Verification', {
            'fields': ('is_verified', 'verified_by')
        }),
    )
    list_per_page = 25


@admin.register(AidRequest)
class AidRequestAdmin(admin.ModelAdmin):
    list_display = ('aid_type', 'requester', 'status', 'priority', 'requested_at')
    list_filter = ('aid_type', 'status', 'priority', 'requested_at')
    search_fields = ('requester__username', 'description')
    readonly_fields = ('requested_at',)
    fieldsets = (
        ('Request Information', {
            'fields': ('requester', 'aid_type', 'disaster_report', 'priority')
        }),
        ('Status', {
            'fields': ('status', 'requested_at', 'approved_by', 'completed_at')
        }),
        ('Details', {
            'fields': ('description', 'people_count')
        }),
    )
    list_per_page = 25
