from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.reverse import reverse


from welcome.models import Profile
from django.contrib.auth.models import User
from welcome.serializers import ProfileSerializer, UserSerializer

# request.POST  # Only handles form data.  Only works for 'POST' method.
# request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
# return Response(data)  # Renders to content type as requested by the client.

# endpoint for root of the api
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        # the reverse function retrieves url details from url's.py file through the name value provided there.
        'users': reverse('user-list', request=request, format=format),
        'profiles': reverse('profile-list', request=request, format=format)
    })
'''
APIViews: 

different from regular View classes:

- Requests passed to the handler methods will be REST framework's Request instances, 
  not Django's HttpRequest instances.
- Handler methods may return REST framework's Response, instead of Django's HttpResponse. 
  The view will manage content negotiation and setting the correct renderer on the response.
- Any APIException exceptions will be caught and mediated into appropriate responses.
  Incoming requests will be authenticated and appropriate permission and/or throttle checks will be run 
  before dispatching the request to the handler method.

'''


class ProfileList(APIView):
    """
    List all user profiles, or create a new user
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # modify how the instance save is managed, and handle any information 
    # that is implicit in the incoming request or requested URL.

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProfileDetail(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    # get the actual user object
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        profile = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        # if deleting the profile, should actually just delete the user
        profile = self.get_object(pk)
        profile.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# ListAPIView & RetrieveAPIView are both read only
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

'''
FUNCTION BASED VIEWS

@api_view(['GET', 'POST'])
# list all user profiles, or create a new user
def user_list(request, format=None):
    if request.method == 'GET':
        users = Profile.objects.all()
        serializer = ProfileSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
# retrieve, update, or delete a user
def user_detail(request, pk, format=None):

    try:
        user = User.objects.get(pk=pk)
        user_profile = Profile.objects.get(user=user)
    except (User.DoesNotExist, Profile.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileSerializer(user_profile, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''

'''
OLD CODE
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

