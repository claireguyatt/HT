from django.shortcuts import HttpResponse, render, redirect
from .models import Profile
from django.contrib.auth import logout

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        context = {
            "data": request.user.profile.get_data().to_html()
        }
        return render(request, 'user/homepage.html', context)
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
