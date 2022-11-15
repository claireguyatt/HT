from django.shortcuts import render, redirect
import pandas as pd
import json

from homepage.models import Variable, Categorical_Variable
# Create your views here.

def index(request):

    context = {
        "variables": request.user.profile.variables.all(),
        "cat_variables": request.user.profile.get_categorical()
    }

    return render(request, 'user/input_data.html', context)

def add_day(request):
    if request.method == "POST":

        request.user.profile.add_day(request.POST)

    return redirect('/homepage')

