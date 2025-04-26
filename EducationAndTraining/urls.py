from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'education_training'

urlpatterns = [
    # Skills Development Program URLs
    path('skills/', views.SkillsProgramListView.as_view(), name='skills_program_list'),
    path('skills/<int:pk>/', views.SkillsProgramDetailView.as_view(), name='skills_program_detail'),

    # Family Welfare Program URLs
    path('family/', views.FamilyProgramListView.as_view(), name='family_program_list'),
    path('family/<int:pk>/', views.FamilyProgramDetailView.as_view(), name='family_program_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)