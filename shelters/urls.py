# 24068022 Soh Kai Xuan
from django.urls import path
from . import views

app_name = 'shelters'

urlpatterns = [
    path('', views.shelter_list, name='shelter_list'),
    path('<int:shelter_id>/', views.shelter_detail, name='shelter_detail'),
]
