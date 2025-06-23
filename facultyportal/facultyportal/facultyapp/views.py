from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from sharedmodels.models import FacultyLogin, FacultyProfile,Teaching,Academics,Positions,AwardHonor, Publication,Project,Guidance
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


# Create your views here.
@login_required
def faculty_dashboard(request):
    user_type = request.session.get('user_type')
    
    if user_type == 'faculty':
        return render(request, 'faculty_dashboard.html')
    else:
        logout(request)
        return redirect("/")
        
def log_out(request):
    logout(request)
    return redirect("home")
    


@login_required
def faculty_profile(request):
    try:
        faculty_login = FacultyLogin.objects.get(email=request.user.email)
    except FacultyLogin.DoesNotExist:
        faculty_login = FacultyLogin.objects.create(email=request.user.email)

    try:
        profile = FacultyProfile.objects.get(login=faculty_login)
    except FacultyProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        contact_number = request.POST.get('contact_number')
        office_number = request.POST.get('office_number')
        about_me = request.POST.get('about_me')
        research_interest = request.POST.get('research_interest')

        profile_photo = request.FILES.get('profile_photo')
        cv_upload = request.FILES.get('cv_upload')
        publications_upload = request.FILES.get('publications_upload')

        if profile:
            profile.name = name
            profile.designation = designation
            profile.department = department
            profile.contact_number = contact_number
            profile.office_number = office_number
            profile.about_me = about_me
            profile.research_interest = research_interest

            if profile_photo:
                profile.profile_photo = profile_photo
            if cv_upload:
                profile.cv_upload = cv_upload
            if publications_upload:
                profile.publications_upload = publications_upload

            profile.save()
        else:
            profile = FacultyProfile.objects.create(
                login=faculty_login,
                name=name,
                designation=designation,
                department=department,
                contact_number=contact_number,
                office_number=office_number,
                about_me=about_me,
                research_interest=research_interest,
                profile_photo=profile_photo,
                cv_upload=cv_upload,
                publications_upload=publications_upload
            )

        return redirect('faculty_profile')

    department_choices = FacultyProfile._meta.get_field('department').choices

    return render(request, 'faculty_profile.html', {
        'profile': profile,
        'department_choices': department_choices
    })


@login_required
def teaching(request):
    try:
        faculty_login = FacultyLogin.objects.get(email=request.user.email)
        faculty_profile = FacultyProfile.objects.get(login=faculty_login)
    except (FacultyLogin.DoesNotExist, FacultyProfile.DoesNotExist):
        return redirect('faculty_profile')

    if request.method == 'POST':
        Teaching.objects.filter(faculty=faculty_profile).delete()

        titles = request.POST.getlist('teaching_description')


        for i in range(len(titles)):
            Teaching.objects.create(
                faculty=faculty_profile,
                teaching_description=titles[i]
            )

        return redirect('teaching')

    teachings = Teaching.objects.filter(faculty=faculty_profile)
    return render(request, 'teaching.html', {'teachings': teachings})

@csrf_exempt
@login_required
def delete_teaching_ajax(request):
    if request.method == 'POST':
        teach_id = request.POST.get('teaching_id')
        try:
            teaching = Teaching.objects.get(id=teach_id)
            teaching.delete()
            return JsonResponse({'success': True})
        except Teaching.DoesNotExist:
            return JsonResponse({'success': False})


@login_required
def academics(request):
    try:
        faculty_login = FacultyLogin.objects.get(email=request.user.email)
        faculty_profile = FacultyProfile.objects.get(login=faculty_login)
    except (FacultyLogin.DoesNotExist, FacultyProfile.DoesNotExist):
        return redirect('faculty_profile')

    if request.method == 'POST':
        submitted_ids = request.POST.getlist('academic_id')
        degrees = request.POST.getlist('academics_description')
        

        # Delete records not in submitted_ids
        existing_ids = [str(academic.id) for academic in faculty_profile.academics.all()]
        for ex_id in existing_ids:
            if ex_id not in submitted_ids:
                Academics.objects.filter(id=ex_id).delete()

        # Update or create entries
        for i in range(len(degrees)):
            academic_id = submitted_ids[i]
            if academic_id:
                academic = Academics.objects.get(id=academic_id, faculty=faculty_profile)
            else:
                academic = Academics(faculty=faculty_profile)
            academic.academics_description = degrees[i]
           
            academic.save()

        return redirect('academics')

    academics_data = faculty_profile.academics.all()
    return render(request, 'academics.html', {
        'academics': academics_data,
    })

@login_required
def delete_academic_ajax(request):
    if request.method == 'POST':
        academic_id = request.POST.get('id')
        try:
            academic = Academics.objects.get(id=academic_id)
            academic.delete()
            return JsonResponse({'success': True})
        except Academics.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Record not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def positions(request):
    try:
        faculty_login = FacultyLogin.objects.get(email=request.user.email)
        faculty_profile = FacultyProfile.objects.get(login=faculty_login)
    except (FacultyLogin.DoesNotExist, FacultyProfile.DoesNotExist):
        return redirect('faculty_profile')

    if request.method == 'POST':
        submitted_ids = request.POST.getlist('position_id')
        roles = request.POST.getlist('roles')
        deleted_ids = request.POST.get('deleted_ids', '')
        

        # Delete marked entries
        if deleted_ids.strip():
            ids_to_delete = [int(i) for i in deleted_ids.split(',') if i.strip().isdigit()]
            Positions.objects.filter(faculty=faculty_profile, id__in=ids_to_delete).delete()

        for pos_id, role in zip(submitted_ids, roles):
            if not role.strip():  # Skip empty entries
                continue

            if pos_id.strip().isdigit():
                Positions.objects.update_or_create(
                    id=int(pos_id.strip()),
                    faculty=faculty_profile,
                    defaults={
                        'roles': role.strip(),
                        
                    }
                )
            else:
                Positions.objects.create(
                    faculty=faculty_profile,
                    roles=role.strip(),
                   
                )

        return redirect('positions')

    existing_positions = Positions.objects.filter(faculty=faculty_profile)
    if not existing_positions.exists():
        existing_positions = []

    return render(request, 'positions.html', {
        'positions': existing_positions
    })


@csrf_exempt
@require_POST
@login_required
def delete_position(request):
    position_id = request.POST.get('position_id')

    try:
        faculty_login = FacultyLogin.objects.get(email=request.user.email)
        faculty_profile = FacultyProfile.objects.get(login=faculty_login)

        if position_id and position_id.strip().isdigit():
            position = Positions.objects.get(id=int(position_id), faculty=faculty_profile)
            position.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid ID'})
    except Positions.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Position not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



@login_required
def award_honors(request):
    try:
        faculty_login = FacultyLogin.objects.get(email=request.user.email)
        faculty_profile = FacultyProfile.objects.get(login=faculty_login)
    except (FacultyLogin.DoesNotExist, FacultyProfile.DoesNotExist):
        return redirect('faculty_profile')

    if request.method == 'POST':
        AwardHonor.objects.filter(faculty=faculty_profile).delete()

        names = request.POST.getlist('name')
        

        for name in names:
            if name.strip():
                AwardHonor.objects.create(
                    faculty=faculty_profile,
                    name=name.strip()
                )
        return redirect('award_honors')

    awards = list(AwardHonor.objects.filter(faculty=faculty_profile))

    # Add one empty entry if no records
    if not awards:
        awards = [None]

    return render(request, 'award_honors.html', {'awards': awards})


@csrf_exempt
@require_POST
@login_required
def delete_award_ajax(request):
    award_id = request.POST.get('award_id')

    try:
        faculty_login = FacultyLogin.objects.get(email=request.user.email)
        faculty_profile = FacultyProfile.objects.get(login=faculty_login)

        if award_id and award_id.strip().isdigit():
            award = AwardHonor.objects.get(id=int(award_id), faculty=faculty_profile)
            award.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid ID'})
    except AwardHonor.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Award not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def publications(request):
    try:
        faculty_login = FacultyLogin.objects.get(email=request.user.email)
        faculty_profile = FacultyProfile.objects.get(login=faculty_login)
    except (FacultyLogin.DoesNotExist, FacultyProfile.DoesNotExist):
        return redirect('faculty_profile')

    if request.method == 'POST':
        Publication.objects.filter(faculty=faculty_profile).delete()

        pub_obj = request.POST.getlist('publications')
        

        for i in range(len(pub_obj)):
            Publication.objects.create(
                faculty=faculty_profile,
                publications=pub_obj[i],
                
            )
        return redirect('publications')

    publications_objects = Publication.objects.filter(faculty=faculty_profile)
    return render(request, 'publications.html', {'publications': publications_objects})

@csrf_exempt
@login_required
def delete_publication_ajax(request):
    if request.method == 'POST':
        pub_id = request.POST.get('publication_id')
        try:
            publication = Publication.objects.get(id=pub_id)
            publication.delete()
            return JsonResponse({'success': True})
        except Publication.DoesNotExist:
            return JsonResponse({'success': False})

@login_required
def projects(request):
    try:
        faculty_login = FacultyLogin.objects.get(email=request.user.email)
        faculty_profile = FacultyProfile.objects.get(login=faculty_login)
    except (FacultyLogin.DoesNotExist, FacultyProfile.DoesNotExist):
        return redirect('faculty_profile')

    if request.method == 'POST':
        # Clear and re-create all project records for the user
        Project.objects.filter(faculty=faculty_profile).delete()

        project_obj = request.POST.getlist('project_description')
        

        for i in range(len(project_obj)):
            if project_obj[i].strip():
                Project.objects.create(
                    faculty=faculty_profile,
                    project_description=project_obj[i],
                    
                )
        return redirect('projects')

    projects = Project.objects.filter(faculty=faculty_profile)
    return render(request, 'projects.html', {'projects': projects})


@csrf_exempt
def delete_project(request):
    if request.method == 'POST':
        project_id = request.POST.get('id')
        try:
            project = Project.objects.get(id=project_id)
            project.delete()
            return JsonResponse({'success': True})
        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Project not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def guidance(request):
    try:
        faculty_login = FacultyLogin.objects.get(email=request.user.email)
        faculty_profile = FacultyProfile.objects.get(login=faculty_login)
    except (FacultyLogin.DoesNotExist, FacultyProfile.DoesNotExist):
        return redirect('faculty_profile')

    if request.method == 'POST':
        # Clear existing records and replace with new
        Guidance.objects.filter(faculty=faculty_profile).delete()

        guidance_obj = request.POST.getlist('guidance_details')
        

        for i in range(len(guidance_obj)):
            Guidance.objects.create(
                faculty=faculty_profile,
                guidance_details=guidance_obj[i],
                
            )

        return redirect('guidance')

    guidances = Guidance.objects.filter(faculty=faculty_profile)
    return render(request, 'guidance.html', {'guidances': guidances})

@login_required
def delete_guidance_ajax(request):
    if request.method == 'POST':
        guidance_id = request.POST.get('guidance_id')
        try:
            guidance = Guidance.objects.get(id=guidance_id)
            guidance.delete()
            return JsonResponse({'success': True})
        except Guidance.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})



