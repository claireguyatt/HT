from xml.dom import ValidationErr
from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .forms import NewUserForm

import logging

def index(request):
    return render(request, 'welcome.html')

# take user to registration page (if GET) or register new user (If POST)
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("Registration successful." )
            return redirect('/homepage')
        print("Unsuccessful registration. Invalid information.")
    return render(request, 'registration/register.html', {'form': NewUserForm})