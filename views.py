from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm
from ngos.models import NGO

def home_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'DONOR':
            return redirect('donor_dashboard')
        elif request.user.role == 'NGO':
            return redirect('ngo_dashboard')
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            if user.role == 'NGO':
                NGO.objects.create(
                    user=user,
                    organization_name=form.cleaned_data['organization_name'],
                    capacity_kg=form.cleaned_data['capacity_kg'] or 50.0,
                    latitude=form.cleaned_data['latitude'],
                    longitude=form.cleaned_data['longitude']
                )
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if user.role == 'DONOR':
                    return redirect('donor_dashboard')
                elif user.role == 'NGO':
                    return redirect('ngo_dashboard')
                else:
                    return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
