from django.shortcuts import render, get_object_or_404
from sharedmodels.models import FacultyLogin, FacultyProfile

def public_faculty_home(request):
    faculties = FacultyProfile.objects.select_related('login').all()
    return render(request, 'home.html', {'faculties': faculties})


def faculty_detail(request, email):
    faculty = get_object_or_404(FacultyProfile, login__email=email)
    return render(request, 'faculty_detail.html', {'faculty': faculty})


# AJAX tab views
def tab_teaching(request, email):
    faculty = get_object_or_404(FacultyProfile, login__email=email)
    return render(request, 'tabs/teaching.html', {'teachings': faculty.teachings.all()})

def tab_academics(request, email):
    faculty = get_object_or_404(FacultyProfile, login__email=email)
    return render(request, 'tabs/academics.html', {'academics': faculty.academics.all()})

def tab_positions(request, email):
    faculty = get_object_or_404(FacultyProfile, login__email=email)
    return render(request, 'tabs/positions.html', {'positions': faculty.positions.all()})

def tab_awards(request, email):
    faculty = get_object_or_404(FacultyProfile, login__email=email)
    return render(request, 'tabs/awards.html', {'awards': faculty.awards.all()})

def tab_publications(request, email):
    faculty = get_object_or_404(FacultyProfile, login__email=email)
    return render(request, 'tabs/publications.html', {'publications': faculty.publications.all()})

def tab_projects(request, email):
    faculty = get_object_or_404(FacultyProfile, login__email=email)
    return render(request, 'tabs/projects.html', {'projects': faculty.projects.all()})

def tab_guidance(request, email):
    faculty = get_object_or_404(FacultyProfile, login__email=email)
    return render(request, 'tabs/guidance.html', {'guidances': faculty.guidances.all()})
