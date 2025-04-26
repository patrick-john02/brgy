from .models import SkillsDevelopmentProgram, FamilyWelfareProgram
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404



# Skills Development Views
class SkillsProgramListView(ListView):
    model = SkillsDevelopmentProgram
    template_name = 'EducationAndTraining/skills_program_list.html'
    context_object_name = 'programs'
    ordering = ['-created_at']


class SkillsProgramDetailView(DetailView):
    model = SkillsDevelopmentProgram
    template_name = 'EducationAndTraining/skills_program_detail.html'
    context_object_name = 'program'


# Family Welfare Views
class FamilyProgramListView(ListView):
    model = FamilyWelfareProgram
    template_name = 'EducationAndTraining/family_program_list.html'
    context_object_name = 'programs'
    ordering = ['-created_at']


class FamilyProgramDetailView(DetailView):
    model = FamilyWelfareProgram
    template_name = 'EducationAndTraining/family_program_detail.html'
    context_object_name = 'program'
