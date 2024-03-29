# django imports
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

# program imports
from .forms import VariableForm
from .models import Variable, CategoricalVariable, ContinuousVariable

def index(request):

    context = {
        "variables": request.user.profile.variables.filter(~Q(name="Happiness")),
        "var_form": VariableForm(),
        "num_vars": request.user.profile.variables.count(),
    }
    return render(request, 'user/edit_variables.html', context)

def delete(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            variable_to_delete = request.POST.get("variable")
            delete_id = request.user.profile.variables.get(name=variable_to_delete).id
            request.user.profile.variables.remove(delete_id)

            # delete associated user data
            df = request.user.profile.get_data()
            var_name = variable_to_delete
            if var_name in df.columns:
                df = df.drop(var_name, axis=1)
                request.user.profile.data = df.to_dict(orient='split')
                request.user.profile.save()
            
            # delete from db if no longer attached to a user profile
            var = Variable.objects.get(id=delete_id)
            var.check_delete()
    
    return redirect('/edit_variables')

def add_variable(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            # make variable
            var_type = request.POST.get("type")
            var_prompt = request.POST.get("prompt")
            var_name = request.POST.get("name")

            # error if name is taken
            if request.user.profile.variables.filter(name=var_name).exists():
                messages.warning(request, "Variable " + var_name + " already exists.")
                return redirect('/edit_variables')

            form = VariableForm(request.POST)

            if form.is_valid():

                if var_type == "binary":
                    new_variable = CategoricalVariable.objects.create(name=var_name, prompt=var_prompt, is_continuous=False, choices="Y,N")
                elif var_type == "categorical":
                    var_choices = request.POST.get("choice")
                    new_variable = CategoricalVariable.objects.create(name=var_name, prompt=var_prompt, is_continuous=False, choices=var_choices, is_binary=False)
                elif var_type == "continuous":
                    start = request.POST.get("start")
                    end = request.POST.get("end")
                    if start >= end:
                        # validation for continuous variable
                        messages.warning(request, "Lower bound must be lower than upper bound for continuous variables. Please try again to create a new variable.")
                        return redirect('/edit_variables')
                    new_variable = ContinuousVariable.objects.create(name=var_name, prompt=var_prompt, is_continuous=True, lower_bound=start, upper_bound=end)
                else:
                    messages.warning(request, "Please select a variable type.")
                    return redirect('/edit_variables')

                request.user.profile.variables.add(new_variable)
            
            else:
                messages.warning(request, form.errors)

    return redirect('/edit_variables')

def edit_choices(request):
    if request.method == "POST":
        variable = CategoricalVariable.objects.get(name=request.POST.get("variable"))
        variable.choices = request.POST.get("choices")
        variable.save()
    return redirect('/edit_variables')