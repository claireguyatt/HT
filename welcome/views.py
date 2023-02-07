from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from welcome.models import Profile
from django.contrib.auth.models import User
from welcome.serializers import ProfileSerializer

# later will need to change csrf_exempt
@csrf_exempt
# list all user profiles, or create a new user
def user_list(request):
    if request.method == 'GET':
        users = Profile.objects.all()
        serializer = ProfileSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
# retrieve, update, or delete a user
def user_detail(request, pk):

    try:
        user = User.objects.get(pk=pk)
        user_profile = Profile.objects.get(user=user)
    except (User.DoesNotExist, Profile.DoesNotExist):
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProfileSerializer(user_profile)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(user_profile, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)


'''
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
'''

