# django imports
from django.shortcuts import render, redirect
from django.contrib import messages

# library imports
from datetime import datetime

# project imports
from welcome.models import User, Profile
from edit_variables.models import Variable
from welcome.forms import validate_date
from homepage.data_analysis.analyze_happiness import Happiness_Analyzer

# Create your views here.

def index(request):
    context = {
        "dob": request.user.profile.dob,
        "gender": request.user.profile.gender
    } 

    return render(request, 'user/settings.html', context)

def change_email(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user.email = request.POST['new_email']
        user.save()
        return render(request, 'user/success.html')
    return redirect('/welcome')

def change_username(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        new_username = request.POST['new_username']
        try:
            user.username = new_username
            user.save()
        except Exception as e:
            messages.add_message(request, messages.WARNING, "Username " + new_username + " is taken. Please try again.")
            return render(request, 'user/settings.html')
        return render(request, 'user/success.html')
    return redirect('/welcome')

def edit_profile(request):
    if request.user.is_authenticated:

        user = User.objects.get(id=request.user.id)

        new_date = datetime.strptime(request.POST.get("new_dob"), '%Y-%m-%d').date()
        try: 
            validate_date(new_date)
            user.profile.dob = new_date
        except Exception as e:
            for errors in e:
                messages.add_message(request, messages.WARNING, errors)
            return render(request, 'user/settings.html')

        user.profile.gender = request.POST.get("new_gender")
        user.profile.save()

        return render(request, 'user/success.html')
    return redirect('/welcome')

def delete_account(request):
    if request.user.is_authenticated:

        user_vars = list(Variable.objects.filter(users=request.user.profile))

        user = User.objects.get(id=request.user.id)
        user.delete()

        # delete associated variables if not attached to another account
        for var in user_vars:
            var.check_delete()

        return redirect('/')

def download_data(request):
    if request.user.is_authenticated:

        user = User.objects.get(id=request.user.id)
        Profile.download_data(user.profile)

        return render(request, 'user/success.html')
    return redirect('/welcome')

