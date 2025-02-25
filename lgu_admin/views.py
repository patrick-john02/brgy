from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from core.models import Service, Project, BarangayOfficial
from django.shortcuts import render, redirect, get_object_or_404
from core.mixins import AdminRequiredMixin
from .forms import ResidentForm, EmployeeAccountForm
from datetime import date
from residents.models import Resident
from core.models import CustomUser

#admin dashboard view
class AdminDashboardView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'lgu_admin/admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

#admin residents list
class AdminResidentsList(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'lgu_admin/residents_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch all residents
        residents = Resident.objects.all()
        
        # Compute age dynamically
        for resident in residents:
            today = date.today()
            resident.age = (
                today.year - resident.birth_date.year -
                ((today.month, today.day) < (resident.birth_date.month, resident.birth_date.day))
            )

        context['residents'] = residents
        context['form'] = ResidentForm()
        return context

#adding New Residents
class AddResidentView(LoginRequiredMixin, AdminRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        form = ResidentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_residents_list')

        return render(request, 'lgu_admin/residents_list.html', {
            'form': form,
            'residents': Resident.objects.all()
        })

#Viewing and Updating Resident Details
class ResidentDetailView(LoginRequiredMixin, AdminRequiredMixin, View):
    """View for displaying and editing resident details."""
    template_name = "lgu_admin/residents_details.html"

    def get(self, request, resident_id):
        resident = get_object_or_404(Resident, id=resident_id)
        today = date.today()
        resident.age = (
            today.year - resident.birth_date.year -
            ((today.month, today.day) < (resident.birth_date.month, resident.birth_date.day))
        )
        return render(request, self.template_name, {'resident': resident})

    def post(self, request, resident_id):
        resident = get_object_or_404(Resident, id=resident_id)

        # Update resident personal details
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

        # Update resident status logic
        resident_status = request.POST.get("resident_status")
        if resident_status == "active":
            resident.is_active = True
        elif resident_status in ["pending", "inactive"]:
            resident.is_active = False  # Either pending or inactive means no login access

        resident.save()
        messages.success(request, "Resident Details Updated Successfully!")
        return redirect('lgu_admin:resident_details', resident_id=resident.id)
    
#admin account list
class AdminAccountList(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    """View for managing employee accounts."""
    
    template_name = "lgu_admin/accounts.html"

    def get_context_data(self, **kwargs):
        """Add employees list and form to context."""
        context = super().get_context_data(**kwargs)
        context["employees"] = CustomUser.objects.filter(user_type="employee")
        context["form"] = EmployeeAccountForm()
        return context

    def post(self, request, *args, **kwargs):
        """Handle account creation when form is submitted."""
        form = EmployeeAccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee account created successfully!")
            return redirect("lgu_admin:account_list")
        else:
            messages.error(request, "Please correct the errors below.")
        
        return self.get(request, *args, **kwargs)

    
    
#admin report list chat app features
class AdminReports(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'lgu_admin/reports.html'
    
#admin barangay clearance view
class AdminBarangayClearance(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'lgu_admin/barangay_clearance.html'

#admin barangay equipment
class AdminBarangayEquipment(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'lgu_admin/equipments.html'

#admin barangay supplies
class AdminBarangaySupplies(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'lgu_admin/supplies.html'
    
#admin resolution
class AdminResolution(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'lgu_admin/resolution.html'

#admin ordinance
class AdminOrdinance(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'lgu_admin/ordinance.html'

#admin memorandum
class AdminMemorandum(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'lgu_admin/memorandum.html'

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

#projects view
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

# officials view
class AdminOfficialsView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'lgu_admin/officials.html'

    def get(self, request):
        officials = BarangayOfficial.objects.all().order_by('-created_at')
        return render(request, self.template_name, {
            'officials': officials, 
            'position_choices': BarangayOfficial.POSITION_CHOICES
        })

    def post(self, request):
        name = request.POST.get('name')
        position = request.POST.get('position')
        description = request.POST.get('description')
        profile_image = request.FILES.get('profile_image')

        if name and position and profile_image:
            BarangayOfficial.objects.create(
                name=name,
                position=position,
                description=description,
                profile_image=profile_image
            )
            messages.success(request, "Official added successfully!")
        else:
            messages.error(request, "All fields are required.")

        return redirect('lgu_admin:official') 
  
#logout function
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Show a success message when the user logs out
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)

    # Redirect to the login page of the core app after logout
    next_page = reverse_lazy('core:login')