# 24068022 Soh Kai Xuan
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Shelter, ShelterRegistration

# Create your views here.
def shelter_list(request):
    """
    View to display a list of all active shelters
    """
    shelters = Shelter.objects.filter(is_active=True).order_by('name')
    context = {
        'shelters': shelters,
        'title': 'Shelter Directory'
    }
    return render(request, 'shelters/shelter_list.html', context)

def shelter_detail(request, shelter_id):
    """
    View to display detailed information about a specific shelter
    """
    shelter = get_object_or_404(Shelter, id=shelter_id, is_active=True)
    context = {
        'shelter': shelter,
        'title': shelter.name
    }
    return render(request, 'shelters/shelter_detail.html', context)
