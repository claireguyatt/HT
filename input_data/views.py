# django imports
from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import ValidationError

# Create your views here.

def index(request):

    context = {
        "variables": request.user.profile.variables.all(),
        "cat_variables": request.user.profile.get_categorical(),
        "con_variables": request.user.profile.get_continuous()
    }

    return render(request, 'user/input_data.html', context)

def add_day(request):
    if request.method == "POST":
        try:
           request.user.profile.add_day(request.POST)
        except ValidationError as v:
            messages.add_message(request, messages.WARNING, str(v)[2:-2])
            return redirect('/input_data')

    return redirect('/homepage')


