from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        if request.user.profile.get_data().empty:
            data = None
        else:
            data = request.user.profile.get_data().to_html()
        context = {
            "data": data
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
