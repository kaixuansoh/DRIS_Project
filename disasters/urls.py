# 24068022 Soh Kai Xuan
from django.urls import path
from . import views

app_name = 'disasters'

urlpatterns = [
    # User-facing URLs
    path('report/submit/', views.submit_disaster_report, name='submit_report'),
    path('reports/', views.my_reports, name='my_reports'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    
    # Aid request URLs
    path('aid/submit/', views.submit_aid_request, name='submit_aid_request'),
    path('aid/requests/', views.my_aid_requests, name='my_aid_requests'),
    path('aid/request/<int:request_id>/', views.aid_request_detail, name='aid_request_detail'),
    
    # Admin management URLs
    path('admin/reports/', views.manage_reports, name='manage_reports'),
    path('admin/report/<int:report_id>/verify/', views.verify_report, name='verify_report'),
    path('admin/report/<int:report_id>/delete/', views.delete_report, name='delete_report'),
    
    # Admin aid management URLs
    path('admin/aid/requests/', views.manage_aid_requests, name='manage_aid_requests'),
    path('admin/aid/request/<int:request_id>/update/', views.update_aid_request, name='update_aid_request'),
]
