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

def edit_variables(request):
    return redirect('/edit_variables')

def input_data(request):
    return redirect('/input_data')

def logout_user(request):
    logout(request)
    return redirect('/')
