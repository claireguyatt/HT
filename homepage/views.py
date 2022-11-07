from django.shortcuts import HttpResponse, render, redirect
from .models import Profile
from django.contrib.auth import logout

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, 'user/homepage.html')
    else:
        return logout_user(request)

def edit_profile(request):
    return render(request, 'user/edit_profile.html')

def logout_user(request):
    logout(request)
    return render(request, 'welcome.html')
