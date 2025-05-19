from .models import SocialWelfareApplication, PwdSeniorServiceRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views import View
from .forms import SocialWelfareApplicationForm
from django.shortcuts import get_object_or_404
from .models import SocialWelfareApplication
from core.mixins import EmployeeRequiredMixin
from core.mixins import AdminRequiredMixin
from core.mixins import ResidentRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect

class SocialWelfareApplicationListView(LoginRequiredMixin,  ListView):
    model = SocialWelfareApplication
    template_name = 'SocialServicesAndWelfare/social_welfare_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return SocialWelfareApplication.objects.filter(resident=self.request.user)

class SocialWelfareApplicationDetailView(LoginRequiredMixin, DetailView):
    model = SocialWelfareApplication
    template_name = 'SocialServicesAndWelfare/social_welfare_application_detail.html'
    context_object_name = 'application'

    def get_queryset(self):
        return SocialWelfareApplication.objects.filter(resident=self.request.user)


class SocialWelfareApplicationCreateView(LoginRequiredMixin, CreateView):
    model = SocialWelfareApplication
    form_class = SocialWelfareApplicationForm
    success_url = reverse_lazy('social_service:social_welfare_applications')

    def form_valid(self, form):
        form.instance.resident = self.request.user
        messages.success(self.request, "Application submitted successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)



# PWD & Senior Services Views
class PwdSeniorServiceRequestListView(LoginRequiredMixin, ListView):
    model = PwdSeniorServiceRequest
    template_name = 'social_service/pwd_senior_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return PwdSeniorServiceRequest.objects.filter(resident=self.request.user)

class PwdSeniorServiceRequestCreateView(LoginRequiredMixin, CreateView):
    model = PwdSeniorServiceRequest
    fields = ['service_type', 'details', 'id_card_upload']
    template_name = 'social_service/pwd_senior_request_form.html'
    success_url = reverse_lazy('social_service:pwd_senior_requests')

    def form_valid(self, form):
        form.instance.resident = self.request.user
        return super().form_valid(form)


#admin side and employee side
class SocialWelfareApplicationAdminListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = SocialWelfareApplication
    template_name = 'SocialServicesAndWelfare/admin/social_welfare_applications_admin.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return SocialWelfareApplication.objects.all()

    def get_template_names(self):
        if self.request.user.user_type == 'admin':
            return ['SocialServicesAndWelfare/admin/social_welfare_applications_admin.html']
        elif self.request.user.user_type == 'employee':
            return ['SocialServicesAndWelfare/employee/social_welfare_applications_employee.html']
        else:
            return ['SocialServicesAndWelfare/social_welfare_applications_default.html']


class SocialWelfareApplicationAdminDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = SocialWelfareApplication
    template_name = 'SocialServicesAndWelfare/admin/social_welfare_application_admin_detail.html'
    context_object_name = 'application'

    def get_queryset(self):
        return SocialWelfareApplication.objects.all()

    def get_template_names(self):
        if self.request.user.user_type == 'admin':
            return ['SocialServicesAndWelfare/admin/social_welfare_application_admin_detail.html']
        elif self.request.user.user_type == 'employee':
            return ['SocialServicesAndWelfare/employee/social_welfare_application_employee_detail.html']
        else:
            return ['SocialServicesAndWelfare/social_welfare_application_default_detail.html']

class SocialWelfareApplicationApproveView(View):
    def post(self, request, pk):
        # Get the application by primary key (ID)
        application = get_object_or_404(SocialWelfareApplication, pk=pk)
        
        # Change the application status to 'approved'
        application.status = 'approved'
        application.save()

        # Add a success message
        messages.success(request, "The application has been approved successfully.")

        # Redirect back to the application list or the application detail page
        return redirect('social_service:social_welfare_application_detail', pk=application.pk)


class SocialWelfareApplicationAdminUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = SocialWelfareApplication
    fields = ['status']
    template_name = 'SocialServicesAndWelfare/admin/social_welfare_application_admin_update.html'
    success_url = reverse_lazy('social_service:social_welfare_applications')

    def form_valid(self, form):
        messages.success(self.request, f"Application status updated to {form.cleaned_data['status']}.")
        return super().form_valid(form)

    def get_template_names(self):
        if self.request.user.user_type == 'admin':
            return ['SocialServicesAndWelfare/admin/social_welfare_application_admin_update.html']
        elif self.request.user.user_type == 'employee':
            return ['SocialServicesAndWelfare/employee/social_welfare_application_employee_update.html']
        else:
            return ['SocialServicesAndWelfare/social_welfare_application_default_update.html']

class SocialWelfareApplicationDeleteView(DeleteView):
    model = SocialWelfareApplication
    success_url = reverse_lazy('social_service:social_welfare_applications')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# PWD & Senior Service Admin Views

class PwdSeniorServiceRequestAdminListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = PwdSeniorServiceRequest
    template_name = 'social_service/admin/pwd_senior_requests_admin.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return PwdSeniorServiceRequest.objects.all()

    def get_template_names(self):
        if self.request.user.user_type == 'admin':
            return ['social_service/admin/pwd_senior_requests_admin.html']
        elif self.request.user.user_type == 'employee':
            return ['social_service/employee/pwd_senior_requests_employee.html']
        else:
            return ['social_service/pwd_senior_requests_default.html']


class PwdSeniorServiceRequestAdminDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = PwdSeniorServiceRequest
    template_name = 'social_service/admin/pwd_senior_request_admin_detail.html'
    context_object_name = 'request'

    def get_queryset(self):
        return PwdSeniorServiceRequest.objects.all()

    def get_template_names(self):
        if self.request.user.user_type == 'admin':
            return ['social_service/admin/pwd_senior_request_admin_detail.html']
        elif self.request.user.user_type == 'employee':
            return ['social_service/employee/pwd_senior_request_employee_detail.html']
        else:
            return ['social_service/pwd_senior_request_default_detail.html']


class PwdSeniorServiceRequestAdminUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = PwdSeniorServiceRequest
    fields = ['status']
    template_name = 'social_service/admin/pwd_senior_request_admin_update.html'
    success_url = reverse_lazy('social_service:pwd_senior_requests')

    def form_valid(self, form):
        messages.success(self.request, f"Request status updated to {form.cleaned_data['status']}.")
        return super().form_valid(form)

    def get_template_names(self):
        if self.request.user.user_type == 'admin':
            return ['social_service/admin/pwd_senior_request_admin_update.html']
        elif self.request.user.user_type == 'employee':
            return ['social_service/employee/pwd_senior_request_employee_update.html']
        else:
            return ['social_service/pwd_senior_request_default_update.html']