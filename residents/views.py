from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from core.mixins import ResidentRequiredMixin
from django.views.generic import DetailView
from django.utils.timezone import localtime
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from core.models import CustomUser
from lgu_admin.models import BarangayAnnouncement
from django.views import View
from django.core.paginator import Paginator
import pytz
from.forms import (JobseekerCertificationForm,
                   CertificateOfGuardianshipForm,
                   CertificateOfGoodMoralCharacterForm,
                   BarangayBusinessCertificateForm,
                   BarangayClearanceForm,
                   CertificationForm,
                   CertificateOfResidencyForm,
                   OneAndSamePersonCertificationForm,
                   CertificateOfUnemploymentForm,
                   CertificateOfIndigencyForm,
                   CertificateOfAppearanceForm,
                   
)
from .models import (
    CertificateOfIndigency,
    JobseekerCertificationRequest,
    CertificateOfGuardianshipRequest,
    CertificateOfGoodMoralCharacterRequest,
    BarangayBusinessCertificateRequest,
    BarangayClearanceRequest,
    CertificationRequest,
    CertificateOfResidency,
    OneAndSamePersonCertification,
    CertificateOfUnemployment,
    CertificateOfAppearance
)

#resident dashboard
class ResidentDashboardView(LoginRequiredMixin, ResidentRequiredMixin, TemplateView):
    template_name = 'residents/resident_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    def get(self, request):
        announcements_list = BarangayAnnouncement.objects.filter(
            is_published=True
        ).order_by('-date_posted')[:5]  # Only show the 5 most recent

        context = {
            'announcements': announcements_list,
        }
        return render(request, 'residents/resident_dashboard.html', context)

class ResidentUploadIDView(LoginRequiredMixin, View):
    template_name = 'residents/unverified_dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        government_id = request.FILES.get('government_id')

        if government_id:
            request.user.government_id = government_id
            request.user.save()
            messages.success(request, "Valid ID uploaded successfully. Please wait for admin verification.")
            return redirect('residents:resident_upload_id')

        messages.error(request, "No file uploaded. Please try again.")
        return render(request, self.template_name)


class ResidentsDocumentRequest(LoginRequiredMixin, ResidentRequiredMixin, View):
    template_name = "residents/document_request.html"

    def get(self, request, *args, **kwargs):
        indigency_form = CertificateOfIndigencyForm()
        jobseeker_form = JobseekerCertificationForm()
        guardianship_form = CertificateOfGuardianshipForm()
        good_moral_form = CertificateOfGoodMoralCharacterForm()
        business_certificate_form = BarangayBusinessCertificateForm()
        barangay_clearance_form = BarangayClearanceForm()
        certification_form = CertificationForm()
        residency_form = CertificateOfResidencyForm()
        one_and_same_person_form = OneAndSamePersonCertificationForm()
        unemployment_form = CertificateOfUnemploymentForm()
        appearance_form = CertificateOfAppearanceForm()
        
        def get (self, request):
            pending_requests = []
            for doc_type, model in self.models.items():
                requests = model.objects.filter(resident=request.user,status="Pending").values('date_requested', 'status').order_by('-date_requested')
            
            for req in requests:
                req['document_type'] = doc_type
                pending_requests.append(req)
            return JsonResponse(pending_requests, safe=False)
                


        return render(request, self.template_name, {
            'indigency_form': indigency_form,
            'jobseeker_form': jobseeker_form,
            'guardianship_form': guardianship_form,
            'good_moral_form': good_moral_form,
            'business_certificate_form': business_certificate_form,
            'barangay_clearance_form': barangay_clearance_form,
            'certification_form': certification_form,
            'residency_form': residency_form,
            'one_and_same_person_form': one_and_same_person_form,
            'unemployment_form': unemployment_form,
            'appearance_form': appearance_form,
        })

    def post(self, request, *args, **kwargs):
        document_type = request.POST.get('document_type')

        if document_type == 'Certificate of Indigency':
            form = CertificateOfIndigencyForm(request.POST)
        elif document_type == 'Jobseeker Certification':
            form = JobseekerCertificationForm(request.POST)
        elif document_type == 'Certificate of Guardianship':
            form = CertificateOfGuardianshipForm(request.POST)
        elif document_type == 'Certificate of Good Moral Character':
            form = CertificateOfGoodMoralCharacterForm(request.POST)
        elif document_type == 'Barangay Business Certificate':
            form = BarangayBusinessCertificateForm(request.POST)
        elif document_type == 'Barangay Clearance':
            form = BarangayClearanceForm(request.POST)
        elif document_type == 'Certification Request':
            form = CertificationForm(request.POST)
        elif document_type == 'Certificate of Residency':
            form = CertificateOfResidencyForm(request.POST)
        elif document_type == 'One and the Same Person Certification':
            form = OneAndSamePersonCertificationForm(request.POST)
        elif document_type == 'Certificate of Unemployment':
            form = CertificateOfUnemploymentForm(request.POST)
        elif document_type == 'Certificate of Appearance':
            form = CertificateOfAppearanceForm(request.POST)
        else:
            form = None

        if form and form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.resident = request.user
            form_instance.save()
            return redirect('residents:dashboard')

        return self.get(request)


class PendingRequestsView(LoginRequiredMixin, View):
    models = {
        'Certificate of Indigency': CertificateOfIndigency,
        'Jobseeker Certification': JobseekerCertificationRequest,
        'Certificate of Guardianship': CertificateOfGuardianshipRequest,
        'Good Moral Certificate': CertificateOfGoodMoralCharacterRequest,
        'Business Certificate': BarangayBusinessCertificateRequest,
        'Barangay Clearance': BarangayClearanceRequest,
        'Certification Request': CertificationRequest,
        'Certificate of Residency': CertificateOfResidency,
        'One and Same Person Certificate': OneAndSamePersonCertification,
        'Unemployment Certificate': CertificateOfUnemployment,
        'Certificate of Appearance': CertificateOfAppearance,
    }

    def get(self, request):
        pending_requests = []

        for doc_type, model in self.models.items():
            requests = model.objects.filter(
                resident=request.user,
                status="Pending"
            ).values('date_requested', 'status').order_by('-date_requested')

            for req in requests:
                req['document_type'] = doc_type
                pending_requests.append(req)

        return JsonResponse(pending_requests, safe=False)


class ApproveRequestsView(LoginRequiredMixin, ResidentRequiredMixin, View):
    models = {
        'Certificate of Indigency': CertificateOfIndigency,
        'Jobseeker Certification': JobseekerCertificationRequest,
        'Certificate of Guardianship': CertificateOfGuardianshipRequest,
        'Good Moral Certificate': CertificateOfGoodMoralCharacterRequest,
        'Business Certificate': BarangayBusinessCertificateRequest,
        'Barangay Clearance': BarangayClearanceRequest,
        'Certification Request': CertificationRequest,
        'Certificate of Residency': CertificateOfResidency,
        'One and Same Person Certificate': OneAndSamePersonCertification,
        'Unemployment Certificate': CertificateOfUnemployment,
        'Certificate of Appearance': CertificateOfAppearance,
    }

    def get(self, request):
        approve_requests = []

        for doc_type, model in self.models.items():
            requests = model.objects.filter(
                resident=request.user,
                status="Approved"
            ).values('date_requested', 'status').order_by('-date_requested')

            for req in requests:
                req['document_type'] = doc_type
                approve_requests.append(req)

        return JsonResponse(approve_requests, safe=False)
    
class RejectedRequestsView(LoginRequiredMixin, ResidentRequiredMixin, View):
    models = {
        'Certificate of Indigency': CertificateOfIndigency,
        'Jobseeker Certification': JobseekerCertificationRequest,
        'Certificate of Guardianship': CertificateOfGuardianshipRequest,
        'Good Moral Certificate': CertificateOfGoodMoralCharacterRequest,
        'Business Certificate': BarangayBusinessCertificateRequest,
        'Barangay Clearance': BarangayClearanceRequest,
        'Certification Request': CertificationRequest,
        'Certificate of Residency': CertificateOfResidency,
        'One and Same Person Certificate': OneAndSamePersonCertification,
        'Unemployment Certificate': CertificateOfUnemployment,
        'Certificate of Appearance': CertificateOfAppearance,
    }

    def get(self, request):
        reject_requests = []

        for doc_type, model in self.models.items():
            requests = model.objects.filter(
                resident=request.user,
                status="Rejected"
            ).values('date_requested', 'status').order_by('-date_requested')

            for req in requests:
                req['document_type'] = doc_type
                reject_requests.append(req)

        return JsonResponse(reject_requests, safe=False)

class ResidentsProfileView(LoginRequiredMixin, ResidentRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'residents/profile.html'
    context_object_name = 'user'
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ViewPrograms(LoginRequiredMixin, ResidentRequiredMixin, TemplateView):
    template_name = 'residents/view_programs.html'

#Submitted Documents
class ResidentDocumentSubmitted(LoginRequiredMixin, ResidentRequiredMixin, TemplateView):
    template_name = 'residents/submitted_documents.html'

#Apply Programs
class ResidentDocumentApplyPrograms(LoginRequiredMixin, ResidentRequiredMixin, TemplateView):
    template_name = 'residents/apply_programs.html'

#borrow
class InventoryBorrow(LoginRequiredMixin, ResidentRequiredMixin, TemplateView):
    template_name = 'residents/inventory_borrow.html'
   
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)

    next_page = reverse_lazy('core:login')
    
    
# Additional utility view for residents to see published announcements
class PublicAnnouncementsView(View):
    """View for residents to see published announcements"""
    
    def get(self, request):
        try:
            # Get only published announcements, ordered by latest first
            announcements_list = BarangayAnnouncement.objects.filter(
                is_published=True
            ).order_by('-date_posted')
            
            # Pagination - 10 announcements per page for public view
            paginator = Paginator(announcements_list, 10)
            page_number = request.GET.get('page', 1)
            announcements = paginator.get_page(page_number)
            
            context = {
                'announcements': announcements,
                'total_announcements': announcements_list.count(),
            }
            
            return render(request, 'public/announcements.html', context)
            
        except Exception as e:
            messages.error(request, f"Error loading announcements: {str(e)}")
            return render(request, 'public/announcements.html', {'announcements': []})
