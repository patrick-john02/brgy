from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from core.mixins import EmployeeRequiredMixin
from core.mixins import ResidentRequiredMixin
from core.mixins import AdminRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import *
from .models import (
    EmergencyContact, HealthIssue, HealthAlertSubscription,
    MedicalAssistanceRequest, HealthServiceProvider, HealthServiceFeedback
)
from .forms import (
    EmergencyContactForm, HealthIssueForm, MedicalAssistanceRequestForm, HealthServiceFeedbackForm
)

#Residents side
class EmergencyContactListView(LoginRequiredMixin, ListView):
    model = EmergencyContact
    template_name = 'HealthandEmergencyServices/emergency_contacts.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)

class EmergencyContactCreateView(LoginRequiredMixin, CreateView):
    model = EmergencyContact
    form_class = EmergencyContactForm
    template_name = 'HealthAndEmergencyServices/contact_form.html'
    success_url = reverse_lazy('health_emergency:emergency_contacts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class HealthIssueListView(LoginRequiredMixin, ResidentRequiredMixin, ListView):
    model = HealthIssue
    template_name = 'HealthAndEmergencyServices/health_issues.html'
    context_object_name = 'issues'

    def get_queryset(self):
        return HealthIssue.objects.filter(user=self.request.user)

class HealthIssueCreateView(LoginRequiredMixin, ResidentRequiredMixin, CreateView):
    model = HealthIssue
    form_class = HealthIssueForm
    template_name = 'HealthAndEmergencyServices/health_issue_form.html'
    success_url = reverse_lazy('health_emergency:health_issues')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MedicalRequestListView(LoginRequiredMixin, ResidentRequiredMixin, ListView):
    model = MedicalAssistanceRequest
    template_name = 'HealthAndEmergencyServices/medical_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return MedicalAssistanceRequest.objects.filter(user=self.request.user)

class MedicalRequestCreateView(LoginRequiredMixin, ResidentRequiredMixin, CreateView):
    model = MedicalAssistanceRequest
    form_class = MedicalAssistanceRequestForm
    template_name = 'HealthAndEmergencyServices/medical_request_form.html'
    success_url = reverse_lazy('health_emergency:medical_requests')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)




#admin side
class AdminEmergencyContactListViews(LoginRequiredMixin, ListView):
    model = EmergencyContact
    template_name = 'HealthAndEmergencyServices/admin/emergency_contact_list.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        return EmergencyContact.objects.all()
    
    def get_template_names(self):
        if self.request.user.user_type == 'admin':
            return ['HealthAndEmergencyServices/admin/emergency_contact_list.html']
        elif self.request.user.user_type == 'employee':
            return ['HealthAndEmergencyServices/employee/emergency_contact_list.html']
        else:
            return ['HealthAndEmergencyServices/emergency_contacts.html']


class EmergencyContactCreateView(LoginRequiredMixin, EmployeeRequiredMixin, AdminRequiredMixin, CreateView):
    model = EmergencyContact
    form_class = EmergencyContactForm
    template_name = 'health_emergency/emergency_contact_form.html'
    success_url = reverse_lazy('health_emergency:emergency_contacts')

class EmergencyContactUpdateView(LoginRequiredMixin, EmployeeRequiredMixin, AdminRequiredMixin, UpdateView):
    model = EmergencyContact
    form_class = EmergencyContactForm
    template_name = 'health_emergency/emergency_contact_form.html'
    success_url = reverse_lazy('health_emergency:emergency_contacts')

class EmergencyContactDeleteView(LoginRequiredMixin, EmployeeRequiredMixin, AdminRequiredMixin, DeleteView):
    model = EmergencyContact
    template_name = 'health_emergency/emergency_contact_confirm_delete.html'
    success_url = reverse_lazy('health_emergency:emergency_contacts')

class HealthIssueListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = HealthIssue
    template_name = 'HealthAndEmergencyServices/admin/health_issue_list.html'
    context_object_name = 'issues'

class HealthIssueCreateView(LoginRequiredMixin, EmployeeRequiredMixin, AdminRequiredMixin, CreateView):
    model = HealthIssue
    form_class = HealthIssueForm
    template_name = 'health_emergency/health_issue_form.html'
    success_url = reverse_lazy('health_emergency:health_issues')

class HealthIssueUpdateView(LoginRequiredMixin, EmployeeRequiredMixin, AdminRequiredMixin, UpdateView):
    model = HealthIssue
    form_class = HealthIssueForm
    template_name = 'HealthAndEmergencyServices/admin/health_issue_form.html'
    success_url = reverse_lazy('health_emergency:health_issues')

class HealthIssueDeleteView(LoginRequiredMixin, EmployeeRequiredMixin, AdminRequiredMixin, DeleteView):
    model = HealthIssue
    template_name = 'health_emergency/health_issue_confirm_delete.html'
    success_url = reverse_lazy('health_emergency:health_issues')

class MedicalAssistanceRequestListView(LoginRequiredMixin, EmployeeRequiredMixin, AdminRequiredMixin, ListView):
    model = MedicalAssistanceRequest
    template_name = 'health_emergency/medical_assistance_request_list.html'
    context_object_name = 'requests'

class MedicalAssistanceRequestCreateView(LoginRequiredMixin, EmployeeRequiredMixin, AdminRequiredMixin, CreateView):
    model = MedicalAssistanceRequest
    form_class = MedicalAssistanceRequestForm
    template_name = 'health_emergency/medical_assistance_request_form.html'
    success_url = reverse_lazy('health_emergency:medical_requests')

class MedicalAssistanceRequestUpdateView(LoginRequiredMixin, EmployeeRequiredMixin, AdminRequiredMixin, UpdateView):
    model = MedicalAssistanceRequest
    form_class = MedicalAssistanceRequestForm
    template_name = 'health_emergency/medical_assistance_request_form.html'
    success_url = reverse_lazy('health_emergency:medical_requests')

class MedicalAssistanceRequestDeleteView(LoginRequiredMixin, EmployeeRequiredMixin, AdminRequiredMixin, DeleteView):
    model = MedicalAssistanceRequest
    template_name = 'health_emergency/medical_assistance_request_confirm_delete.html'
    success_url = reverse_lazy('health_emergency:medical_requests')