from django.shortcuts import render, redirect
from django.contrib import messages

from datetime import datetime

from welcome.models import User
from edit_variables.models import Variable
from welcome.forms import validate_date

# Create your views here.

def index(request):
    print(request.user.profile.dob)
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
        user.username = request.POST['new_username']
        user.save()
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
            print(e)
            messages.warning(request, e)
            print(messages)
            return render(request, 'user/settings.html')

        user.profile.dob = new_date
        
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


