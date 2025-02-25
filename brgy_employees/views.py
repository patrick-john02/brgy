from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from core.mixins import EmployeeRequiredMixin

class EmployeeDashboardView(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = 'brgy_employees/employee_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class ManageResidentList(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = 'brgy_employees/residents_list.html'

class EmployeeManageReports(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = 'brgy_employees/incidents_reports.html'

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