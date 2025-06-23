from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from sharedmodels.models import FacultyLogin
from django.contrib import messages

def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    user_email = request.user.email

    # Check if user is in AdminLogin table
    if FacultyLogin.objects.filter(email=user_email).exists():
        request.session['user_type'] = 'faculty'
        request.session['admin_email'] = user_email
        return redirect('facultyapp/faculty_dashboard/')
    
    # If email not found, log out
    else:
        logout(request)
        messages.error(request, "Access denied: email not registered.",extra_tags="access_denied")
        return redirect("home")

