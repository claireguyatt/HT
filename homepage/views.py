from django.shortcuts import HttpResponse, render, redirect
from .models import Profile
from django.contrib.auth import logout

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, 'user/homepage.html')
    else:
        return logout_user(request)

def settings(request):
    return redirect('/settings')

def input_data(request):
    return render(request, 'user/input_data.html')

def logout_user(request):
    logout(request)
    return redirect('/')
