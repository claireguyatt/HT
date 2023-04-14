# django imports
from django.shortcuts import render, redirect
from django.contrib.auth import logout

# program imports
from .data_analysis.analyze_happiness import Happiness_Analyzer

def index(request):
    if request.user.is_authenticated:
        if request.user.profile.get_data().empty:
            data = None
            days = None
        else:
            all_data = request.user.profile.get_data()
            days = all_data.index
            data = all_data.to_html()

        context = {
            "data": data,
            "days": days
        }
        return render(request, 'user/homepage.html', context)
    else:
        return logout_user(request)

def delete_data(request):
    if request.user.is_authenticated:
        print(type(request.POST.keys()))
        if 'day' in request.POST.keys():
            day = request.POST['day']
            request.user.profile.delete_data(day)
        else:
            request.user.profile.delete_data("all")
    
    return redirect('/homepage')

def settings(request):
    return redirect('/settings')

def edit_variables(request):
    return redirect('/edit_variables')

def input_data(request):
    return redirect('/input_data')

def logout_user(request):

    # TO-DO if guest user, revert back to original (unsave all changes)

    logout(request)
    return redirect('/')

def analyze(request):
    if request.user.is_authenticated:
        analyzer = Happiness_Analyzer(request.user.profile.get_data())
        print(analyzer.data)
        analyzer.preprocess()
        context = {
            "analysis":analyzer.linera_reg()
        }
    return redirect('/homepage', context)

