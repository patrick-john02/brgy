from .forms import ResidentForm, UserAccountForm, EditUserAccountForm,ResidentProfileForm, ResidentAccountForm, UserProfileForm, PasswordChangeForm
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView, UpdateView, FormView
from .models import ChatThread, Message, InventoryCategory, InventoryItem
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from core.models import Service, Project, BarangayOfficial
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models.functions import ExtractYear
from residents.models import Resident, Household
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy, reverse
from core.mixins import AdminRequiredMixin
from core.models import BarangayOfficial
from django.core.mail import send_mail
from django.utils.timezone import now
from django.contrib import messages
from core.models import CustomUser
from django.db.models import Count
from django.utils import timezone
from django.conf import settings
from datetime import date
#residents app folder importations
from residents.models import (
    CertificateOfIndigency, JobseekerCertificationRequest, CertificateOfGuardianshipRequest,
    CertificateOfGoodMoralCharacterRequest, BarangayBusinessCertificateRequest,
    BarangayClearanceRequest, CertificationRequest, CertificateOfResidency,
    OneAndSamePersonCertification, CertificateOfUnemployment, CertificateOfAppearance, Resident,
)

class AdminDashboardView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'lgu_admin/admin_dashboard.html'

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
    
class AdminProfileView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'lgu_admin/profile.html'
    context_object_name = 'user'
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditAdminProfileView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'lgu_admin/edit_profile.html'
    success_url = reverse_lazy('lgu_admin:admin_profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)


class ChangeAdminPasswordView(LoginRequiredMixin, AdminRequiredMixin, FormView):
    form_class = PasswordChangeForm
    template_name = 'lgu_admin/change_password.html'
    success_url = reverse_lazy('lgu_admin:admin_profile')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Password changed successfully!')
        return super().form_valid(form)
#end of profile admin 


class AdminResidentsList(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'lgu_admin/residents_list.html'

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



class AddResidentView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        resident_form = ResidentForm()
        profile_form = ResidentProfileForm()
        residents = Resident.objects.all()
        households = Household.objects.all()
        
        return render(request, 'lgu_admin/residents_list.html', {
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
            return redirect('lgu_admin:residents_list')

        print("Resident Form Errors:", resident_form.errors)
        print("Profile Form Errors:", profile_form.errors)

        messages.error(request, "Failed to add resident. Please check the form and try again.")
        return render(request, 'lgu_admin/residents_list.html', {
            'resident_form': resident_form,
            'profile_form': profile_form,
            'residents': Resident.objects.all(),
            'households': Household.objects.all(),
        })

#Viewing and Updating Resident Details
class ResidentDetailView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = "lgu_admin/residents_details.html"

    def get(self, request, resident_id):
        """Displays resident details along with household and profile information."""
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
        return redirect('lgu_admin:resident_details', resident_id=resident.id)



class ArchivedResidentsListView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = "lgu_admin/resident_archives.html"

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

class ArchiveResidentView(LoginRequiredMixin, AdminRequiredMixin, View):

    def post(self, request, resident_id):
        resident = get_object_or_404(Resident, id=resident_id)
        resident.is_archived = True
        resident.save()

        full_name = f"{resident.first_name} {resident.middle_name} {resident.last_name}".strip()
        messages.success(request, f"Resident {full_name} archived successfully!")
        return redirect("lgu_admin:archived_residents")

class UnarchiveResidentView(LoginRequiredMixin, AdminRequiredMixin, View):
    
    def post(self, request, resident_id):
        resident = get_object_or_404(Resident, id=resident_id)
        resident.is_archived = False
        resident.save()

        full_name = f"{resident.first_name} {resident.middle_name or ''} {resident.last_name}".strip()
        if resident.suffix:
            full_name += f" {resident.suffix}"

        messages.success(request, f"Resident {full_name} restored successfully!")
        return redirect("lgu_admin:archived_residents")
    
class UnverifiedResidentsListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = CustomUser
    template_name = 'lgu_admin/vefication.html'
    context_object_name = 'users'

    def get_queryset(self):
        return CustomUser.objects.filter(is_verified=False, user_type='resident', is_deleted=False)

class ApproveResidentView(View):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        if user.user_type == 'resident':
            user.is_verified = True
            user.save()
            return JsonResponse({"success": True, "message": "User approved successfully."})
        return JsonResponse({"success": False, "message": "Invalid user."})

class AdminAccountList(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = "lgu_admin/accounts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = CustomUser.objects.filter(is_superuser=False, is_deleted=False)
        context["form"] = UserAccountForm()
        return context

    def post(self, request, *args, **kwargs):
        form = UserAccountForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "User account created successfully! Login details have been sent to the user's email.")
            return redirect("lgu_admin:account_list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        context = self.get_context_data()
        context["form"] = form
        return render(request, self.template_name, context)
    
class AdminResidentAccountList(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = "lgu_admin/vefication.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = CustomUser.objects.filter(user_type='resident', is_deleted=False)
        context["form"] = ResidentAccountForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ResidentAccountForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()

            subject = "Your Barangay System Account Credentials"
            message = (
                f"Hello {user.first_name} {user.last_name},\n\n"
                f"Your Resident Account has been successfully created.\n\n"
                f"Username: {user.username}\n"
                f"Password: {user.raw_password}\n"
                f"User Type: {user.get_user_type_display()}\n\n"
                f"Please change your password after logging in.\n\n"
                f"Best Regards,\nBarangay System Admin"
            )
            send_mail(subject, message, 'your_email@example.com', [user.email])

            messages.success(request, "Resident account created successfully!")
            return redirect("lgu_admin:residents_list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        context = self.get_context_data()
        context["form"] = form
        return render(request, self.template_name, context)


class UserDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'lgu_admin/employee_edit.html'
    context_object_name = 'user'

def verify_resident(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if user.user_type == 'resident' and not user.is_verified:
        user.is_verified = True
        user.save()

        send_mail(
            subject='Account Verified ✔️',
            message=f'Hello {user.first_name} {user.last_name},\n\n'
                    'Your account has been successfully verified by the LGU Admin.\n\n'
                    'You can now access the system with full functionality.\n\n'
                    'Thank you!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(request, f'{user.first_name} {user.last_name} has been successfully verified.')
    else:
        messages.error(request, 'This user cannot be verified.')

    return redirect('lgu_admin:view_user', pk=pk)

#edit resident details
class UserDetailViews(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'lgu_admin/unverified_res.html'
    context_object_name = 'user'

def verify_resident(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if user.user_type == 'resident' and not user.is_verified:
        user.is_verified = True
        user.save()

        send_mail(
            subject='Account Verified ✔️',
            message=f'Hello {user.first_name} {user.last_name},\n\n'
                    'Your account has been successfully verified by the LGU Admin.\n\n'
                    'You can now access the system with full functionality.\n\n'
                    'Thank you!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        messages.success(request, f'{user.first_name} {user.last_name} has been successfully verified.')
    else:
        messages.error(request, 'This user cannot be verified.')
    return redirect('lgu_admin:view_user_residents', pk=pk)

        
# Edit Employee Details
class EditEmployeeView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditUserAccountForm
    template_name = "lgu_admin/employee_edit.html"
    context_object_name = "employee"

    def get_success_url(self):
        messages.success(self.request, "Employee details updated successfully!")
        return reverse_lazy("lgu_admin:account_list")
    

class EditEmployeeViews(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditUserAccountForm
    template_name = "lgu_admin/unverified_res.html"
    context_object_name = "residents"

    def get_success_url(self):
        messages.success(self.request, "residents account details updated successfully!")
        return reverse_lazy("lgu_admin:view_user_residents")
    
    def approve_user(request, pk):
        if request.method == 'POST':
            user = get_object_or_404(CustomUser, pk=pk)
            try:
                user.is_verified = True
                user.save()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

class DeleteUserView(View):

    def post(self, request, user_id):
        if request.user.user_type != "admin":
            return JsonResponse({"success": False, "error": "Only admins can delete users."}, status=403)

        user = get_object_or_404(CustomUser, pk=user_id)

        if request.user == user:
            return JsonResponse({"success": False, "error": "You cannot delete your own account."}, status=400)

        user.delete()
        return JsonResponse({"success": True, "message": "User deleted successfully."})

# Admin Report List (Reports sent to Admin)
class AdminReportsView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ChatThread
    template_name = "lgu_admin/reports.html"
    context_object_name = "report_threads"

    def get_queryset(self):
        if self.request.user.user_type != 'admin':  
            return ChatThread.objects.none()
        
        return ChatThread.objects.filter(messages__is_report=True).distinct()


#Chat List View (List all chat threads of the user)
class ChatListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ChatThread
    template_name = "chat/chat_list.html"
    context_object_name = "chat_threads"

    def get_queryset(self):
        user = self.request.user
        return ChatThread.objects.filter(user1=user) | ChatThread.objects.filter(user2=user)

# Chat Detail View (Retrieve messages from a thread)
class ChatDetailView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, thread_id):
        thread = get_object_or_404(ChatThread, id=thread_id)
        
        if request.user not in [thread.user1, thread.user2]:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        messages = Message.objects.filter(thread=thread).order_by("timestamp")

        return JsonResponse({
            "messages": [
                {
                    "content": msg.content,
                    "sender": msg.sender.username,
                    "timestamp": msg.timestamp.strftime("%I:%M %p"),
                }
                for msg in messages
            ]
        })


# for messeging features
class SendMessageView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        receiver = get_object_or_404(CustomUser, id=kwargs["user_id"])
        
        if request.user == receiver:
            return JsonResponse({"error": "You cannot message yourself"}, status=400)

        thread, created = ChatThread.get_or_create_thread(request.user, receiver)
        
        content = request.POST.get("content")
        is_report = request.POST.get("is_report") == "true"
        
        if content:
            message = Message.objects.create(
                thread=thread,
                sender=request.user,
                receiver=receiver,
                content=content,
                is_report=is_report
            )
            return JsonResponse({
                "message": message.content,
                "sender": message.sender.username,
                "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "is_report": message.is_report
            })
        return JsonResponse({"error": "Message content cannot be empty"}, status=400)

#admin barangay Document view
class AdminBarangayClearance(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'lgu_admin/barangay_clearance.html'

class AdminPendingRequestsView(LoginRequiredMixin, AdminRequiredMixin, View):
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



class PrintCertificateView(View, AdminRequiredMixin, LoginRequiredMixin ):
    DOCUMENT_TEMPLATES = {
        "Jobseeker Certification": "lgu_admin/certificate.html",
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
        template = self.DOCUMENT_TEMPLATES.get(document_type, "lgu_admin/certificate.html")

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

class ApproveCertificationView(View,LoginRequiredMixin, AdminRequiredMixin ):
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
            print(f"Error: Invalid document type - {document_type}")  # Debugging
            return JsonResponse({"error": "Invalid document type"}, status=400)

        try:
            cert_request = model.objects.get(id=request_id)
            print(f"Found {document_type} request with ID: {request_id}")  # Debugging
        except model.DoesNotExist:
            print(f"❌ Error: {document_type} request with ID {request_id} not found!")  # Debugging
            return JsonResponse({"error": f"{document_type} request not found"}, status=404)

        cert_request.status = "Approved"
        cert_request.date_approved = now()
        cert_request.save()

        print(f"Successfully approved {document_type} with ID: {request_id}")  # Debugging

        # return JsonResponse({
        #     "message": f"{document_type} approved successfully",
        #     "status": cert_request.status,
        #     "date_approved": cert_request.date_approved.strftime('%B %d, %Y')
        # })
        
        return redirect(reverse('lgu_admin:brgy_clearance'))



class AdminApprovedRequestsView(AdminRequiredMixin, LoginRequiredMixin, View):
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

class AdminRejectedRequestsView(AdminRequiredMixin, LoginRequiredMixin, View):
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
    
#admin barangay equipment
class AdminBarangayEquipment(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'lgu_admin/equipments.html'

#admin barangay supplies
# class AdminBarangaySupplies(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
#     template_name = 'lgu_admin/supplies.html'
    
#admin resolution
# class AdminResolution(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
#     template_name = 'lgu_admin/resolution.html'

#admin ordinance
# class AdminOrdinance(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
#     template_name = 'lgu_admin/ordinance.html'

#admin memorandum
# class AdminMemorandum(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
#     template_name = 'lgu_admin/memorandum.html'

#services view
class AdminServicesView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'lgu_admin/services.html'

    def get(self, request):
        services = Service.objects.all().order_by('-created_at')
        return render(request, self.template_name, {'services': services})

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if title and description and image:
            Service.objects.create(title=title, description=description, image=image)
            messages.success(request, "Service added successfully!")
        else:
            messages.error(request, "All fields are required.")

        return redirect('lgu_admin:service')

#services update view
class ServiceUpdateView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk):
        service = get_object_or_404(Service, pk=pk)

        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        if title and description:
            service.title = title
            service.description = description
            if image:
                service.image = image
            service.save()

            return JsonResponse({"success": True, "message": "Service updated successfully!"})

        return JsonResponse({"success": False, "errors": "All fields are required."}, status=400)

class ServiceDeleteView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        service.delete()

        return JsonResponse({"success": True, "message": "Service deleted successfully!"})

class AdminProjectsView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'lgu_admin/programs.html'

    def get(self, request):
        projects = Project.objects.all().order_by('-created_at')
        return render(request, self.template_name, {'projects': projects})

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if title and description and image:
            Project.objects.create(title=title, description=description, image=image)
            messages.success(request, "Project added successfully!")
        else:
            messages.error(request, "All fields are required.")
        return redirect('lgu_admin:project')

class EditProjectView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'lgu_admin/edit_project.html'

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        return render(request, self.template_name, {'project': project})

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if title and description:
            project.title = title
            project.description = description

            if image:
                project.image = image

            project.save()
            messages.success(request, "Project updated successfully!")
        else:
            messages.error(request, "All fields are required.")

        return redirect('lgu_admin:project')

class DeleteProjectView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect('lgu_admin:project')

class AdminOfficialsView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'lgu_admin/officials.html'

    def get(self, request):
        employees = CustomUser.objects.filter(user_type='employee', is_deleted=False)
        officials = BarangayOfficial.objects.all().order_by('-created_at')

        return render(request, self.template_name, {
            'officials': officials,
            'position_choices': BarangayOfficial.POSITION_CHOICES,
            'users': employees,
        })

    def post(self, request):
        name = request.POST.get('name')
        position = request.POST.get('position')
        description = request.POST.get('description')
        profile_image = request.FILES.get('profile_image')
        user_id = request.POST.get('user_id')

        if name and position and profile_image and user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
                if user.user_type != 'employee':
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'message': 'Selected user is not an employee.'})
                    messages.error(request, "Selected user is not an employee.")
                    return redirect('lgu_admin:official')

                if BarangayOfficial.objects.filter(user=user).exists():
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'message': 'This employee has already posted as an official.'})
                    messages.error(request, "This employee has already posted as an official.")
                    return redirect('lgu_admin:official')

                BarangayOfficial.objects.create(
                    user=user,
                    position=position,
                    description=description,
                    profile_image=profile_image
                )

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'Official added successfully!'})
                messages.success(request, "Official added successfully!")
            
            except CustomUser.DoesNotExist:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'User not found.'})
                messages.error(request, "User not found.")
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'All fields are required.'})
            messages.error(request, "All fields are required.")

        # Redirect back for non-AJAX requests
        return redirect('lgu_admin:official')

class DeleteOfficialView(View, LoginRequiredMixin, AdminRequiredMixin ):
    def post(self, request):
        official_id = request.POST.get('id')
        print(f"Official ID: {official_id}")  # Debug print statement

        if not official_id:
            return JsonResponse({'success': False, 'message': 'No ID provided.'})

        try:
            official = BarangayOfficial.objects.get(id=official_id)
            official.delete() 
            return JsonResponse({'success': True})
        
        except BarangayOfficial.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Official not found.'})

        
#INVENTORY LOGIC
class InventoryCategoryView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'lgu_admin/equipments.html'

    def get(self, request):
        categories = InventoryCategory.objects.all()
        return render(request, self.template_name, {'categories': categories})

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description', '')

        if name:
            InventoryCategory.objects.create(name=name, description=description)
            messages.success(request, "Category added successfully!")
        else:
            messages.error(request, "Category name is required.")

        return redirect('lgu_admin:inventory_categories')

class InventoryItemView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'lgu_admin/equipments.html'

    def get(self, request):
        items = InventoryItem.objects.select_related('category').all()
        categories = InventoryCategory.objects.all()
        return render(request, self.template_name, {
            'items': items,
            'categories': categories,
        })

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        quantity = request.POST.get('quantity')
        unit = request.POST.get('unit', 'pcs')
        critical_level = request.POST.get('critical_level', 5)

        if name and category_id and quantity:
            try:
                category = InventoryCategory.objects.get(id=category_id)
                InventoryItem.objects.create(
                    name=name,
                    description=description,
                    category=category,
                    quantity=int(quantity),
                    unit=unit,
                    critical_level=int(critical_level)
                )
                messages.success(request, "Item added successfully!")
            except InventoryCategory.DoesNotExist:
                messages.error(request, "Category not found.")
        else:
            messages.error(request, "All required fields must be filled.")

        return redirect('lgu_admin:inventory_items')

class InventoryItemUpdateView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, item_id):
        try:
            item = InventoryItem.objects.get(id=item_id)
        except InventoryItem.DoesNotExist:
            messages.error(request, "Item not found.")
            return redirect('lgu_admin:inventory_items')

        item.name = request.POST.get('name')
        item.description = request.POST.get('description', '')
        item.unit = request.POST.get('unit', 'pcs')
        item.quantity = request.POST.get('quantity', 0)
        item.critical_level = request.POST.get('critical_level', 5)

        category_id = request.POST.get('category')
        try:
            item.category = InventoryCategory.objects.get(id=category_id)
        except InventoryCategory.DoesNotExist:
            messages.error(request, "Selected category does not exist.")
            return redirect('lgu_admin:inventory_items')

        item.save()
        messages.success(request, "Item updated successfully!")
        return redirect('lgu_admin:inventory_items')

#logout function
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)

    next_page = reverse_lazy('core:login')