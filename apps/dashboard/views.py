from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Dispatcher View
@login_required
def homeView(request):
    """
    Acts as a router. Checks the user's group and redirects 
    to the appropriate dashboard.
    """
    if request.user.groups.filter(name='Managers').exists():
        return redirect('dashboard:manager-dashboard')
    else:
        return redirect('dashboard:user-dashboard')

# User Dashboard
@login_required
def user_dashboard(request):
    return render(request, 'dashboard/home.html')

# Manager Dashboard
@login_required
def manager_dashboard(request):
    # Fetch data relevant to managers
    total_users = User.objects.count()
    new_users_count = User.objects.filter(is_active=True).count()
    recent_users = User.objects.select_related('user_profile').order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'new_users_count': new_users_count,
        'recent_users': recent_users
    }
    return render(request, 'dashboard/manager_home.html', context)