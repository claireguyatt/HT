from email.utils import format_datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.messages import get_messages

from .forms import NewUserForm
from homepage.models import Profile, Variable

def index(request):
    return render(request, 'welcome.html')

# take user to registration page (if GET) or register new user (if POST)
def register(request):
    
    if request.user.is_authenticated:
        return redirect('/homepage')
    if request.method == "POST":
        
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # make user profile
            profile = Profile.objects.create(user=user, username=user.username, 
                    email=user.email, dob=form.cleaned_data['dob'], number=form.cleaned_data['number'], 
                    gender=form.cleaned_data['gender'])

            # add default variables to profile
            default_vars = ["Happiness", "Sleep", "Temp", "Weather"]
            for var in default_vars:
                v = Variable.objects.get(name=var)
                profile.variables.add(v)

            profile.save()
            login(request, user)
            print("Registration successful.")
            return redirect('/homepage')

        messages.warning(request, form.errors)
        print("Unsuccessful registration. Invalid information.")
        
    return render(request, 'registration/register.html', {'form': NewUserForm})