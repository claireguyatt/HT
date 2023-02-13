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