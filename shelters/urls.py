# 24068022 Soh Kai Xuan
from django.urls import path
from . import views

app_name = 'shelters'

urlpatterns = [
    path('', views.shelter_list, name='shelter_list'),
    path('<int:shelter_id>/', views.shelter_detail, name='shelter_detail'),
    # Shelter Management URLs
    path('manage/', views.manage_shelters, name='manage_shelters'),
    path('add/', views.add_shelter, name='add_shelter'),
    path('edit/<int:shelter_id>/', views.edit_shelter, name='edit_shelter'),
    path('delete/<int:shelter_id>/', views.delete_shelter, name='delete_shelter'),
]
