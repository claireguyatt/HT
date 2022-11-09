from email.utils import format_datetime
from xml.dom import ValidationErr
from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth import login
from django.contrib import messages
import datetime

from .forms import NewUserForm
from homepage.models import Profile

def index(request):
    return render(request, 'welcome.html')

# take user to registration page (if GET) or register new user (If POST)
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            print(user)
            profile = Profile.objects.create(user=user, username=user.username, 
                    email=user.email, dob=form.cleaned_data['dob'], number=form.cleaned_data['number'], 
                    gender=form.cleaned_data['gender'])
            profile.save()

            login(request, user)
            print("Registration successful.")
            return redirect('/homepage')
        print(form.error_messages)
        print("Unsuccessful registration. Invalid information.")
    return render(request, 'registration/register.html', {'form': NewUserForm})