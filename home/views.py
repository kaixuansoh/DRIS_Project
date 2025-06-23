# 24068022 Soh Kai Xuan
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home/index.html'
