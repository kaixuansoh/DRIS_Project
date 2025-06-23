# 24068022 Soh Kai Xuan
from django.urls import path
from . import views

app_name = 'disasters'

urlpatterns = [
    # User-facing URLs
    path('report/submit/', views.submit_disaster_report, name='submit_report'),
    path('reports/', views.my_reports, name='my_reports'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    
    # Admin management URLs
    path('admin/reports/', views.manage_reports, name='manage_reports'),
    path('admin/report/<int:report_id>/verify/', views.verify_report, name='verify_report'),
    path('admin/report/<int:report_id>/delete/', views.delete_report, name='delete_report'),
]
