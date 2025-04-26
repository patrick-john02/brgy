from django.views.generic import ListView, CreateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import (
    EmergencyContact, HealthIssue, HealthAlertSubscription,
    MedicalAssistanceRequest, HealthServiceProvider, HealthServiceFeedback
)
from .forms import (
    EmergencyContactForm, HealthIssueForm, MedicalAssistanceRequestForm, HealthServiceFeedbackForm
)

# Emergency Contacts
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

# Health Issues
class HealthIssueListView(LoginRequiredMixin, ListView):
    model = HealthIssue
    template_name = 'HealthAndEmergencyServices/health_issues.html'
    context_object_name = 'issues'

    def get_queryset(self):
        return HealthIssue.objects.filter(user=self.request.user)

class HealthIssueCreateView(LoginRequiredMixin, CreateView):
    model = HealthIssue
    form_class = HealthIssueForm
    template_name = 'HealthAndEmergencyServices/health_issue_form.html'
    success_url = reverse_lazy('health_emergency:health_issues')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Medical Assistance Requests
class MedicalRequestListView(LoginRequiredMixin, ListView):
    model = MedicalAssistanceRequest
    template_name = 'HealthAndEmergencyServices/medical_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return MedicalAssistanceRequest.objects.filter(user=self.request.user)

class MedicalRequestCreateView(LoginRequiredMixin, CreateView):
    model = MedicalAssistanceRequest
    form_class = MedicalAssistanceRequestForm
    template_name = 'HealthAndEmergencyServices/medical_request_form.html'
    success_url = reverse_lazy('health_emergency:medical_requests')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
