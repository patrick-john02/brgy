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