from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .forms import NewUserForm
from .models import Profile, User

def index(request):
    return render(request, 'welcome.html')

# take user to registration page or register new user
def register(request):
    
    if request.user.is_authenticated:
        return redirect('/homepage')

    if request.method == "POST":

        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # make user profile
            profile = Profile.objects.create_profile(user=user, username=user.username, 
                    email=user.email, dob=form.cleaned_data['dob'], number=form.cleaned_data['number'], 
                    gender=form.cleaned_data['gender'])

            profile.save()
            login(request, user)
            print("Registration successful.")
            return redirect('/homepage')

        for errors in form.errors.items():
            messages.add_message(request, messages.WARNING, errors)
            
        print("Unsuccessful registration. Invalid information.")
        
    return render(request, 'registration/register.html', {'form': NewUserForm})

# signs in with guest account, deletes changes on logout
# to fix in future: could be problematic if more than one guest at once
def explore(request):

    user = User.objects.get(username="Guest")
    login(request, user)
    return redirect('/homepage')

