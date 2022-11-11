from django.shortcuts import render, redirect
from django.db.models import Q

from homepage.models import Variable

# Create your views here.

def index(request):
    
    context = {
        "variables": request.user.profile.variables.filter(~Q(name="Happiness"))
    }
    return render(request, 'user/edit_variables.html', context)

def delete(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            variable_to_delete = request.POST.get("variable")
            delete_id = Variable.objects.get(name=variable_to_delete).id
            request.user.profile.variables.remove(delete_id)
            return redirect('/edit_variables')

def add_variable(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # can't make variable with same name
            var_name = request.POST.get("name")
            if Variable.objects.all().filter(name=var_name).exists():
                print("variable name already exists, please choose another")
                return redirect('/edit_variables')
            # can't go over 10 variables (excluding happiness)
            if request.user.profile.variables.all().count() > 10:
                print("cann't add more than 10 variables")
                return redirect('/edit_variables')
            var_prompt = request.POST.get("prompt")
            new_variable = Variable.objects.create(name=var_name, prompt=var_prompt)
            request.user.profile.variables.add(new_variable)
    return redirect('/edit_variables')