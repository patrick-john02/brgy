from django.views.generic import TemplateView, View, ListView, DetailView, CreateView, UpdateView, FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import ExtractYear
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from core.mixins import EmployeeRequiredMixin
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count
from datetime import date
from django.http import JsonResponse


from lgu_admin.models import InventoryItem
from residents.models import (
    CertificateOfIndigency, JobseekerCertificationRequest, CertificateOfGuardianshipRequest,
    CertificateOfGoodMoralCharacterRequest, BarangayBusinessCertificateRequest,
    BarangayClearanceRequest, CertificationRequest, CertificateOfResidency,
    OneAndSamePersonCertification, CertificateOfUnemployment, CertificateOfAppearance, Resident,Household, 
)
from lgu_admin.forms import (
    ResidentForm, 
    UserAccountForm, 
    EditUserAccountForm,
    ResidentProfileForm, 
    ResidentAccountForm, 
    UserProfileForm, 
    PasswordChangeForm
)

class EmployeeDashboardView(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = 'brgy_employees/employee_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['active_residents_count'] = Resident.objects.filter(is_active=True).count()

        context['document_requests_count'] = (
            CertificateOfIndigency.objects.filter(status="Pending").count() +
            JobseekerCertificationRequest.objects.filter(status="Pending").count() +
            CertificateOfGuardianshipRequest.objects.filter(status="Pending").count() +
            CertificateOfGoodMoralCharacterRequest.objects.filter(status="Pending").count() +
            BarangayBusinessCertificateRequest.objects.filter(status="Pending").count() +
            BarangayClearanceRequest.objects.filter(status="Pending").count() +
            CertificationRequest.objects.filter(status="Pending").count() +
            CertificateOfResidency.objects.filter(status="Pending").count() +
            OneAndSamePersonCertification.objects.filter(status="Pending").count() +
            CertificateOfUnemployment.objects.filter(status="Pending").count() +
            CertificateOfAppearance.objects.filter(status="Pending").count()
        )

        # Count inventory items
        context['inventory_count'] = InventoryItem.objects.count()
        residents_by_year = (
            Resident.objects
            .filter(is_active=True, date_registered__year__gte=2019)
            .annotate(year=ExtractYear('date_registered'))
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )
        context['residents_by_year'] = residents_by_year

        return context

class ManageResidentList(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = 'brgy_employees/residents_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        residents = Resident.objects.filter(is_archived=False)

        context['households'] = Household.objects.all()
        
        for resident in residents:
            today = date.today()
            resident.age = (
                today.year - resident.birth_date.year -
                ((today.month, today.day) < (resident.birth_date.month, resident.birth_date.day))
            )

            full_name_parts = [resident.first_name]
            if resident.middle_name:
                full_name_parts.append(resident.middle_name)
            full_name_parts.append(resident.last_name)
            if resident.suffix:
                full_name_parts.append(resident.suffix)
            resident.full_name = " ".join(full_name_parts)

        context['residents'] = residents
        context['form'] = ResidentForm()
        return context

class AddResidentView(LoginRequiredMixin, EmployeeRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        resident_form = ResidentForm()
        profile_form = ResidentProfileForm()
        residents = Resident.objects.all()
        households = Household.objects.all()
        
        return render(request, 'brgy_employees/residents_list.html', {
            'resident_form': resident_form,
            'profile_form': profile_form,
            'residents': residents,
            'households': households,
        })

    def post(self, request, *args, **kwargs):
        
        resident_form = ResidentForm(request.POST)
        profile_form = ResidentProfileForm(request.POST, request.FILES)

        if resident_form.is_valid() and profile_form.is_valid():
            id_number = resident_form.cleaned_data['id_number']

            if Resident.objects.filter(id_number=id_number).exists():
                messages.error(request, "Resident with this ID number already exists.")
                return redirect('residents_list')

            household_number = request.POST.get('household_number', '').strip()
            household_address = request.POST.get('household_address', '').strip()

            household = None
            if household_number:
                household, created = Household.objects.get_or_create(
                    household_number=household_number,
                    defaults={'address': household_address if household_address else 'Unknown Address'}
                )
                if not created and not household.address and household_address:
                    household.address = household_address
                    household.save()

            resident = resident_form.save(commit=False)
            resident.household = household  
            resident.save()

            profile = profile_form.save(commit=False)
            profile.resident = resident
            profile.occupation = request.POST.get('occupation', '').strip()
            profile.save()

            messages.success(request, f"Resident {resident.first_name} {resident.last_name} added successfully!")
            return redirect('brgy_employees:residents_list')

        print("Resident Form Errors:", resident_form.errors)
        print("Profile Form Errors:", profile_form.errors)

        messages.error(request, "Failed to add resident. Please check the form and try again.")
        return render(request, 'brgy_employees/residents_list.html', {
            'resident_form': resident_form,
            'profile_form': profile_form,
            'residents': Resident.objects.all(),
            'households': Household.objects.all(),
        })

class ResidentDetailView(LoginRequiredMixin, EmployeeRequiredMixin, View):
    template_name = "brgy_employees/residents_details.html"

    def get(self, request, resident_id):
        resident = get_object_or_404(Resident, id=resident_id)
        today = now().date()
        resident.age = (
            today.year - resident.birth_date.year -
            ((today.month, today.day) < (resident.birth_date.month, resident.birth_date.day))
        )
        profile = getattr(resident, "profile", None)
        household = resident.household if resident.household else None
        household_address = household.address if household else "No Address Provided"
        households = Household.objects.all()
        return render(request, self.template_name, {
            'resident': resident,
            'profile': profile,
            'household': household,
            'household_number': household.household_number if household else "",
            'household_address': household_address,
            'households': households,
            'is_head_of_family': profile.is_head_of_family if profile else False,
            'is_pwd': profile.is_pwd if profile else False,
            'is_senior_citizen': profile.is_senior_citizen if profile else False,
            'government_id': profile.government_id.url if profile and profile.government_id else None,
        })

    def post(self, request, resident_id):
        resident = get_object_or_404(Resident, id=resident_id)
        profile = getattr(resident, "profile", None)

        resident.first_name = request.POST.get("first_name")
        resident.middle_name = request.POST.get("middle_name", "")
        resident.last_name = request.POST.get("last_name")
        resident.suffix = request.POST.get("suffix", "")
        resident.birth_date = request.POST.get("birth_date")
        resident.place_of_birth = request.POST.get("place_of_birth")
        resident.gender = request.POST.get("gender")
        resident.nationality = request.POST.get("nationality")
        resident.civil_status = request.POST.get("civil_status")
        resident.address = request.POST.get("address")
        resident.barangay_zone = request.POST.get("barangay_zone")
        resident.contact_number = request.POST.get("contact_number")
        resident.voter_status = request.POST.get("voter_status") == "True"
        resident.id_number = request.POST.get("id_number", "").strip()

        household_number = request.POST.get("household", "").strip()
        if household_number:
            household, created = Household.objects.get_or_create(household_number=household_number)
            resident.household = household

        resident_status = request.POST.get("resident_status")
        resident.is_active = resident_status == "active"

        if profile:
            profile.occupation = request.POST.get("occupation", "").strip()
            profile.is_head_of_family = request.POST.get("is_head_of_family") == "on"
            profile.is_pwd = request.POST.get("is_pwd") == "on"
            profile.is_senior_citizen = request.POST.get("is_senior_citizen") == "on"

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            if 'government_id' in request.FILES:
                profile.government_id = request.FILES['government_id']
            profile.save()

        resident.save()
        messages.success(request, "Resident Details Updated Successfully!")
        return redirect('brgy_employees:resident_details', resident_id=resident.id)

class ArchivedResidentsListView(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = "brgy_employees/resident_archives.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        residents = Resident.objects.filter(is_archived=True)

        for resident in residents:
            full_name_parts = [resident.first_name]
            if resident.middle_name:
                full_name_parts.append(resident.middle_name)
            full_name_parts.append(resident.last_name)
            if resident.suffix:
                full_name_parts.append(resident.suffix)
            resident.full_name = " ".join(full_name_parts)

        context['residents'] = residents
        return context

class ArchiveResidentView(LoginRequiredMixin, EmployeeRequiredMixin, View):
    def post(self, request, resident_id):
        resident = get_object_or_404(Resident, id=resident_id)
        resident.is_archived = True
        resident.save()

        full_name = f"{resident.first_name} {resident.middle_name} {resident.last_name}".strip()
        messages.success(request, f"Resident {full_name} archived successfully!")
        return redirect("brgy_employees:archived_residents")

class UnarchiveResidentView(LoginRequiredMixin, EmployeeRequiredMixin, View):
    def post(self, request, resident_id):
        resident = get_object_or_404(Resident, id=resident_id)
        resident.is_archived = False
        resident.save()

        full_name = f"{resident.first_name} {resident.middle_name or ''} {resident.last_name}".strip()
        if resident.suffix:
            full_name += f" {resident.suffix}"

        messages.success(request, f"Resident {full_name} restored successfully!")
        return redirect("brgy_employees:archived_residents")

#start of employee clearance requests 
class EmployeeBarangayClearance(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = 'brgy_employees/barangay_clearance.html'
    

class EmployeePendingRequestsView(LoginRequiredMixin, EmployeeRequiredMixin, View):
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
            requests = model.objects.filter(status="Pending").select_related('resident').values(
                'id', 'date_requested', 'status', 
                'resident__id', 'resident__first_name', 'resident__middle_name', 
                'resident__last_name', 'resident__suffix'
            ).order_by('-date_requested')

            for req in requests:
                req['document_type'] = doc_type
                req['resident_name'] = f"{req['resident__first_name']} {req['resident__middle_name'] or ''} {req['resident__last_name']} {req['resident__suffix'] or ''}".strip()
                pending_requests.append(req)

        return JsonResponse(pending_requests, safe=False)

class PrintCertificateView(View, EmployeeRequiredMixin, LoginRequiredMixin ):
    DOCUMENT_TEMPLATES = {
        "Jobseeker Certification": "brgy_employees/certificate.html",
        "Certificate of Guardianship": "certification/guardianship_certificate.html",
        "Good Moral Certificate": "certification/good_moral_certificate.html",
        "Business Certificate": "certification/business_certificate.html",
        "Barangay Clearance": "certification/barangay_clearance.html",
        "Certification Request": "certification/certification_request.html",
        "Certificate of Residency": "certification/residency_certificate.html",
        "One and Same Person Certificate": "certification/one_and_same_person_certificate.html",
        "Unemployment Certificate": "certification/unemployment_certificate.html",
        "Certificate of Indigency": "certification/indigency_certificate.html",
        "Certificate of Appearance": "certification/appearance_certificate.html",
    }
    DOCUMENT_MODELS = {
        "Jobseeker Certification": JobseekerCertificationRequest,
        "Certificate of Guardianship": CertificateOfGuardianshipRequest,
        "Good Moral Certificate": CertificateOfGoodMoralCharacterRequest,
        "Business Certificate": BarangayBusinessCertificateRequest,
        "Barangay Clearance": BarangayClearanceRequest,
        "Certification Request": CertificationRequest,
        "Certificate of Residency": CertificateOfResidency,
        "One and Same Person Certificate": OneAndSamePersonCertification,
        "Unemployment Certificate": CertificateOfUnemployment,
        "Certificate of Indigency": CertificateOfIndigency,
        "Certificate of Appearance": CertificateOfAppearance,
    }

    def get(self, request, document_type, request_id):
        model = self.DOCUMENT_MODELS.get(document_type)
        template = self.DOCUMENT_TEMPLATES.get(document_type, "brgy_employees/certificate.html")

        if not model:
            return JsonResponse({"error": "Invalid document type"}, status=400)

        try:
            req = model.objects.get(id=request_id)
            print(f"✅ Found {document_type} with ID: {request_id}")  # Debugging
        except model.DoesNotExist:
            print(f"❌ Error: {document_type} with ID {request_id} not found!")  # Debugging
            return JsonResponse({"error": f"{document_type} not found"}, status=404)

        resident_full_name = " ".join([name for name in [
            req.resident.first_name,
            req.resident.middle_name if req.resident.middle_name else None,
            req.resident.last_name,
            req.resident.suffix if req.resident.suffix else None
        ] if name])

        context = {
            "resident_full_name": resident_full_name,
            "document_type": document_type,
            "request_id": req.id,
            "issued_date": req.date_approved.strftime('%B %d, %Y') if req.date_approved else "________",
            "approved_by": req.approved_by if req.approved_by else "________",
            "barangay_official_witness": req.barangay_official_witness if req.barangay_official_witness else "________",
        }

        # **Document-specific context**
        if document_type == "Jobseeker Certification":
            context.update({
                "purok": req.purok or "N/A",
                "years_of_residency": req.years_of_residency,
                "months_of_residency": req.months_of_residency,
                "status": req.status,
            })

        elif document_type == "Certificate of Guardianship":
            context.update({
                "resident_name": resident_full_name,
                "guardian_name": req.guardian_name or "N/A",
                "birthday": req.birthday.strftime('%B %d, %Y') if req.birthday else "N/A",
                "place_of_birth": req.place_of_birth or "N/A",
            })

        elif document_type == "Good Moral Certificate":
            context.update({
                "resident_name": resident_full_name,
                "purpose": req.purpose or "Barangay Community Check",
            })

        elif document_type == "Business Certificate":
            context.update({
                "resident_name": resident_full_name,
                "line_of_business": req.line_of_business or "________",
                "res_cert_no": req.res_cert_no if req.res_cert_no else "________",
                "place_of_issue": req.place_of_issue if req.place_of_issue else "________",
                "or_no": req.or_no if req.or_no else "________",
            })
        
        elif document_type == "Barangay Clearance": 
            context.update({
                "resident_name": resident_full_name,
                "reason_for_request": req.reason_for_request or "________",
                "status": req.status,
            })
        
        elif document_type == "Certification Request":
            context.update({
                "resident_name": resident_full_name,
                "sex": req.sex or "________",
                "age": req.age,
                "color": req.color or "________",
                "brand_owner": req.brand_owner or "________",
                "brand_municipality": req.brand_municipality or "________",
                "item_sold_to": req.item_sold_to or "________",
                "sold_amount": req.sold_amount or "________",
                "certification_purpose": req.certification_purpose or "________",
                "status": req.status,
            })
        
        elif document_type == "Certificate of Residency": 
            context.update({
                "resident_name": resident_full_name,
                "age": req.age,
                "civil_status": req.civil_status or "________",
                "purpose": req.purpose or "________",
                "status": req.status,
            })
            
        elif document_type == "One and Same Person Certificate":
            context.update({
                "resident_name": resident_full_name,
                "name_one": req.name_one or "________",
                "name_two": req.name_two or "________",
                "full_name": req.full_name or "________",
                "sex": req.sex,
                "purpose": req.purpose or "________",
                "status": req.status,
            })
        
        elif document_type == "Certificate of Unemployment":
            context.update({
                "resident_name": resident_full_name,
                "full_name": req.full_name or "________",
                "sex": req.sex,
                "civil_status": req.civil_status,
                "purok": req.purok or "________",
                "status": req.status,
            })
        
        elif document_type == "Certificate of Indigency":
            context.update({
                "resident_name": resident_full_name,
                "full_name": req.full_name or "________",
                "sex": req.sex,
                "purok": req.purok or "________",
                "status": req.status,
            })
        
        elif document_type == "Certificate of Appearance":
            context.update({
                "resident_name": resident_full_name,
                "full_name": req.full_name or "________",
                "designation": req.designation or "________",
                "office_agency": req.office_agency or "________",
                "purpose": req.purpose or "________",
                "date_of_appearance": req.date_of_appearance.strftime('%B %d, %Y') if req.date_of_appearance else "________",
                "status": req.status,
            })

        return render(request, template, context)

class ApproveCertificationView(View,LoginRequiredMixin, EmployeeRequiredMixin ):
    MODELS = {
        "Jobseeker Certification": JobseekerCertificationRequest,
        "Certificate of Guardianship": CertificateOfGuardianshipRequest,
        'Good Moral Certificate': CertificateOfGoodMoralCharacterRequest,
        'Business Certificate': BarangayBusinessCertificateRequest,
        'Barangay Clearance': BarangayClearanceRequest,
        'Certification Request': CertificationRequest,
        'Certificate of Residency': CertificateOfResidency,
        'One and Same Person Certificate': OneAndSamePersonCertification,
        'Unemployment Certificate': CertificateOfUnemployment,
        'Certificate of Appearance': CertificateOfAppearance,
    }
    def post(self, request, request_id):
        document_type = request.POST.get("document_type")  
        model = self.MODELS.get(document_type)

        if not model:
            print(f"❌ Error: Invalid document type - {document_type}")  # Debugging
            return JsonResponse({"error": "Invalid document type"}, status=400)

        try:
            cert_request = model.objects.get(id=request_id)
            print(f"✅ Found {document_type} request with ID: {request_id}")  # Debugging
        except model.DoesNotExist:
            print(f"❌ Error: {document_type} request with ID {request_id} not found!")  # Debugging
            return JsonResponse({"error": f"{document_type} request not found"}, status=404)

        # Update the status to Approved
        cert_request.status = "Approved"
        cert_request.date_approved = now()
        cert_request.save()

        print(f"✅ Successfully approved {document_type} with ID: {request_id}")  # Debugging

        return JsonResponse({
            "message": f"{document_type} approved successfully",
            "status": cert_request.status,
            "date_approved": cert_request.date_approved.strftime('%B %d, %Y')
        })



class EmployeeApprovedRequestsView(EmployeeRequiredMixin, LoginRequiredMixin, View):
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
        approved_request = []

        for doc_type, model in self.models.items():
            requests = model.objects.filter(status="Approved").values('date_requested', 'status').order_by('-date_requested')
            for req in requests:
                req['document_type'] = doc_type
                approved_request.append(req)

        return JsonResponse(approved_request, safe=False)

class EmployeeRejectedRequestsView(EmployeeRequiredMixin, LoginRequiredMixin, View):
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
        approved_request = []

        for doc_type, model in self.models.items():
            requests = model.objects.filter(status="Rejected").values('date_requested', 'status').order_by('-date_requested')
            for req in requests:
                req['document_type'] = doc_type
                approved_request.append(req)

        return JsonResponse(approved_request, safe=False)

class EmployeeManageReports(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = 'brgy_employees/incidents_reports.html'


# class ProcessDocumentRequestView(LoginRequiredMixin, View):
#     """Allow barangay employees to process document requests."""

#     def get(self, request):
#         if not hasattr(request.user, 'employee_profile'):
#             messages.error(request, "You are not authorized to process requests.")
#             return redirect('brgy_employees:dashboard')

#         pending_requests = DocumentRequest.objects.filter(status='pending')
#         return render(request, 'brgy_employees/process_requests.html', {'pending_requests': pending_requests})

#     def post(self, request, request_id):
#         document_request = get_object_or_404(DocumentRequest, id=request_id)
        
#         if not hasattr(request.user, 'employee_profile'):
#             messages.error(request, "You are not authorized to process requests.")
#             return redirect('brgy_employees:dashboard')

#         action = request.POST.get('action')
#         if action == 'approve':
#             document_request.status = 'approved'
#             document_request.date_processed = now()
#             document_request.processed_by = request.user.employee_profile
#             messages.success(request, "Document request approved successfully.")
#         elif action == 'reject':
#             document_request.status = 'rejected'
#             document_request.date_processed = now()
#             document_request.processed_by = request.user.employee_profile
#             messages.warning(request, "Document request rejected.")
#         else:
#             messages.error(request, "Invalid action.")

#         document_request.save()
#         return redirect('brgy_employees:process_requests')

class EmployeeManageRequest(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = 'brgy_employees/residents_request.html'
    
class EmployeeResolution(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = 'brgy_employees/resolution_request.html'

class EmployeeOrdinance(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = 'brgy_employees/ordinance_request.html'
    
class EmployeeManageProgram(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = 'brgy_employees/programs.html'
    
class EmployeeManageEquipment(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = 'brgy_employees/equipments.html'

class EmployeeManageSupplies(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = 'brgy_employees/supplies.html'

#this is the logout function in employee app 
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)

    next_page = reverse_lazy('core:login')