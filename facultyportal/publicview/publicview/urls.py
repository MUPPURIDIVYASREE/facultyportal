from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.public_faculty_home, name='faculty_home'),

    path('faculty/<str:email>/', views.faculty_detail, name='faculty_detail'),

   
    path('api/faculty/<str:email>/teaching/', views.tab_teaching, name='tab_teaching'),
    path('api/faculty/<str:email>/academics/', views.tab_academics, name='tab_academics'),
    path('api/faculty/<str:email>/positions/', views.tab_positions, name='tab_positions'),
    path('api/faculty/<str:email>/honors/', views.tab_awards, name='tab_awards'),
    path('api/faculty/<str:email>/projects/', views.tab_projects, name='tab_projects'),
    path('api/faculty/<str:email>/guidance/', views.tab_guidance, name='tab_guidance'),
    path('api/faculty/<str:email>/publications/', views.tab_publications, name='tab_publications'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
