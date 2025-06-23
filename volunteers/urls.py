# 24068022 Soh Kai Xuan
from django.urls import path
from . import views

app_name = 'volunteers'

urlpatterns = [
    # Volunteer Availability URLs
    path('availability/', views.availability_list, name='availability_list'),
    path('availability/update/', views.update_availability, name='update_availability'),
    path('availability/edit/<int:availability_id>/', views.edit_availability, name='edit_availability'),
    path('availability/delete/<int:availability_id>/', views.delete_availability, name='delete_availability'),
    
    # Volunteer Assignment URLs
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/status/<int:assignment_id>/<str:new_status>/', views.update_assignment_status, name='update_assignment_status'),
    
    # Authority Assignment Management URLs
    path('manage/assignments/', views.manage_assignments, name='manage_assignments'),
    path('manage/assignments/create/', views.create_assignment, name='create_assignment'),
    path('manage/assignments/edit/<int:assignment_id>/', views.edit_assignment, name='edit_assignment'),
    path('manage/assignments/cancel/<int:assignment_id>/', views.cancel_assignment, name='cancel_assignment'),
]
