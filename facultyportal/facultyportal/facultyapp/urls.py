from django.urls import path
from . import views

urlpatterns = [
    path('faculty_dashboard/', views.faculty_dashboard, name= "faculty_dashboard"),
    path('faculty_dashboard/faculty_profile',views.faculty_profile, name="faculty_profile"),
    path('faculty_dashboard/teaching/', views.teaching, name='teaching'),
    path('faculty_dashboard/delete_teaching_ajax/', views.delete_teaching_ajax, name='delete_teaching_ajax'),
    path('faculty_dashboard/academics/', views.academics, name='academics'),
    path('faculty_dashboard/delete-academic/', views.delete_academic_ajax, name='delete_academic_ajax'),
    path('faculty_dashboard/positions/', views.positions, name='positions'),
    path('faculty_dashboard/delete_position/', views.delete_position, name='delete_position'),
    path('faculty_dashboard/awards/', views.award_honors, name='award_honors'),
    path('faculty_dashboard/delete_award_ajax/', views.delete_award_ajax, name='delete_award_ajax'),
    path('faculty_dashboard/publications/', views.publications, name='publications'),
    path('faculty_dashboard/delete_publication_ajax/', views.delete_publication_ajax, name='delete_publication_ajax'),
    path('faculty_dashboard/projects/', views.projects, name='projects'),
    path('faculty_dashboard/delete_project/', views.delete_project, name='delete_project'),
    path('faculty_dashboard/guidance/', views.guidance, name='guidance'),
    path('faculty_dashboard/delete_guidance/', views.delete_guidance_ajax, name='delete_guidance_ajax'),
    path('faculty_dashboard/log_out/', views.log_out,name="log_out"),
]
   
   
