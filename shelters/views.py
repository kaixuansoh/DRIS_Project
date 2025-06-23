# 24068022 Soh Kai Xuan
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from .models import Shelter, ShelterRegistration
from .forms import ShelterForm

# Helper function to check if user is authority
def is_authority(user):
    return user.is_authenticated and user.is_authority()

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

@login_required
@user_passes_test(is_authority)
def manage_shelters(request):
    """
    View to list all shelters for management by authorities
    """
    shelters = Shelter.objects.all().order_by('-is_active', 'name')
    context = {
        'shelters': shelters,
        'title': 'Manage Shelters'
    }
    return render(request, 'shelters/manage_shelters.html', context)

@login_required
@user_passes_test(is_authority)
def add_shelter(request):
    """
    View to add a new shelter
    """
    if request.method == 'POST':
        form = ShelterForm(request.POST)
        if form.is_valid():
            shelter = form.save()
            messages.success(request, f"Shelter '{shelter.name}' has been created successfully.")
            return redirect('shelters:manage_shelters')
    else:
        form = ShelterForm()
    
    context = {
        'form': form,
        'title': 'Add New Shelter',
        'is_add': True,
    }
    return render(request, 'shelters/shelter_form.html', context)

@login_required
@user_passes_test(is_authority)
def edit_shelter(request, shelter_id):
    """
    View to edit an existing shelter
    """
    shelter = get_object_or_404(Shelter, id=shelter_id)
    
    if request.method == 'POST':
        form = ShelterForm(request.POST, instance=shelter)
        if form.is_valid():
            shelter = form.save()
            messages.success(request, f"Shelter '{shelter.name}' has been updated successfully.")
            return redirect('shelters:manage_shelters')
    else:
        form = ShelterForm(instance=shelter)
    
    context = {
        'form': form,
        'title': f'Edit Shelter: {shelter.name}',
        'shelter': shelter,
        'is_add': False,
    }
    return render(request, 'shelters/shelter_form.html', context)

@login_required
@user_passes_test(is_authority)
def delete_shelter(request, shelter_id):
    """
    View to delete a shelter
    """
    shelter = get_object_or_404(Shelter, id=shelter_id)
    
    if request.method == 'POST':
        shelter_name = shelter.name
        shelter.delete()
        messages.success(request, f"Shelter '{shelter_name}' has been deleted successfully.")
        return redirect('shelters:manage_shelters')
    
    context = {
        'shelter': shelter,
        'title': f'Delete Shelter: {shelter.name}'
    }
    return render(request, 'shelters/delete_shelter.html', context)
