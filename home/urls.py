# 24068022 Soh Kai Xuan
from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]
