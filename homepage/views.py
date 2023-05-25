# django imports
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages

# program imports
from .data_analysis.analyze_happiness import Happiness_Analyzer

def index(request):
    if request.user.is_authenticated:
        if request.user.profile.get_data().empty:
            data = None
            days = None
            analysis = None
        else:
            all_data = request.user.profile.get_data()
            days = all_data.index
            data = all_data.to_html()
            analysis = request.user.profile.analysis

        context = {
            "data": data,
            "days": days,
            "analysis": analysis
        }
        return render(request, 'user/homepage.html', context)
    else:
        return logout_user(request)

def delete_data(request):
    if request.user.is_authenticated:
        print(request.POST.keys())
        try:
            if 'start_delete_date' in request.POST.keys():
                start_delete_date = request.POST['start_delete_date']
                if 'end_delete_date' in request.POST.keys():
                    end_delete_date = request.POST['end_delete_date']
                    request.user.profile.delete_data_from_range(start_delete_date, end_delete_date)
                else:
                    request.user.profile.delete_data(start_delete_date)
            else:
                request.user.profile.delete_data("all")
        except Exception as e:
            for errors in e:
                messages.add_message(request, messages.WARNING, errors)
            return render(request, 'user/homepage.html')
    
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
        
        pass

    return redirect('/homepage')

