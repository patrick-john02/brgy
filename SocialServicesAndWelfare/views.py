from .models import SocialWelfareApplication, PwdSeniorServiceRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView
from .forms import SocialWelfareApplicationForm
from django.shortcuts import get_object_or_404
from .models import SocialWelfareApplication
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render

class SocialWelfareApplicationListView(LoginRequiredMixin, ListView):
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




