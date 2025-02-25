from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from core.mixins import ResidentRequiredMixin
# from .forms import BarangayClearanceForm

#resident dashboard
class ResidentDashboardView(LoginRequiredMixin, ResidentRequiredMixin, TemplateView):
    template_name = 'residents/resident_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

#resident barangay requests
# class RequestBarangayClearance(LoginRequiredMixin, View):
#     template_name = 'residents/barangay_clearance.html'

#     def get(self, request):
#         form = BarangayClearanceForm()
#         return render(request, self.template_name, {'form': form})
    
#     def post(self, request):
#         form = BarangayClearanceForm(request.POST)
#         if form.is_valid():
#             if not request.user.resident_profile:  # Ensure resident_profile exists
#                 messages.error(request, "Your account is not linked to a resident profile.")
#                 return redirect('core:error')  

#             clearance_request = form.save(commit=False)
#             clearance_request.resident = request.user.resident_profile
#             clearance_request.save()
#             messages.success(request, "Your barangay clearance request has been submitted successfully!")
#             return redirect('residents:barangay_clearance')
#         return render(request, self.template_name, {'form': form})


# class ViewPrograms(LoginRequiredMixin, TemplateView):
#     template_name = 'residents/view_programs.html'

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