from django.shortcuts import render, redirect

from welcome.models import User
from edit_variables.models import Variable

# Create your views here.

def index(request):
    return render(request, 'user/settings.html')

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
        if request.POST.get("new_dob"):
            user.profile.dob = request.POST.get("new_dob")
        if request.POST.get("new_gender"):
            user.profile.dob = request.POST.get("gender")
        user.save()
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


