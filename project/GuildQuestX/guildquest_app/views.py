from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    print("rendering index..")
    return render(request, 'guildquest_app/index')

@login_required
def dashboard(request):
    user = request.user

    # check and render based on role

    if hasattr(user, 'manager'):
        return render(request, 'polls/dashboards/manager.html', {'user' : user})
    
    elif hasattr(user, 'employee'):
        return render(request, 'polls/dashboards/employee.html', {'user' : user})
    
    elif hasattr(user, 'payrollteam'):
        return render(request, 'polls/dashboards/payrollteam.html', {'user' : user})
    
    elif hasattr(user, 'teamleader'):
        return render(request, 'polls/dashboards/teamleader.html', {'user' : user})
    
#For guest users who are not logged in.
def dashboard_guest(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'polls/guest.html', {'message': "No content. Please sign in first."})
    