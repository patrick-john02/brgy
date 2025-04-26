from .models import Service, Project, BarangayOfficial, CustomUser
from .forms import BarangayReportForm, CustomUserRegistrationForm
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import make_password
from django.views.generic import TemplateView, View
from residents.models import Resident, Household
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from lgu_admin.models import BarangayReport
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
import openai
import json

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'core/login.html'

    def get_redirect_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.user_type == 'admin':
                return reverse('lgu_admin:dashboard')
            elif user.user_type == 'employee':
                return reverse('brgy_employees:dashboard')
            elif user.user_type == 'resident':
                return reverse('residents:dashboard')
            else:
                messages.error(self.request, "User type not recognized.")
                return reverse('core:login')
        return super().get_redirect_url()


class LandingPageView(View):
    template_name = "core/landingpage.html"

    def get(self, request):
        context = {
            "form": BarangayReportForm(),  # Pass the form to the template
            "total_male": Resident.objects.filter(gender="M", is_active=True).count(),
            "total_female": Resident.objects.filter(gender="F", is_active=True).count(),
            "total_population": Resident.objects.filter(is_active=True).count(),
            "total_households": Household.objects.count(),
            "services": Service.objects.all(),
            "projects": Project.objects.all(),
            "brgy_officials": BarangayOfficial.objects.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = BarangayReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.image = request.FILES.get("image", None)
            report.save()
            messages.success(request, "Your report has been submitted successfully.")
        else:
            messages.error(request, "There was an error with your submission. Please check the form.")

        return redirect("core:landing")


class ResidentRegistrationView(View):
    template_name = 'core/registration.html'

    def get(self, request):
        form = CustomUserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name'] or ''
            last_name = form.cleaned_data['last_name']
            suffix = form.cleaned_data['suffix'] or ''

            query = Q(
                first_name__iexact=first_name,
                last_name__iexact=last_name
            )
            
            if middle_name:
                query &= Q(middle_name__iexact=middle_name)
            
            if suffix:
                query &= Q(suffix__iexact=suffix)
                
            try:
                resident = Resident.objects.get(query)
                
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.user_type = 'resident'
                    
                    user.save()
                    
                login(request, user)
                messages.success(request, "Registration successful. Welcome!")
                return redirect('residents:resident_dashboard')
                
            except Resident.DoesNotExist:
                messages.error(request, "Sorry, you are not registered on the list. Please inquire in our respective barangay.")
            except Resident.MultipleObjectsReturned:
                messages.error(request, "Multiple resident records found. Please contact the barangay office for assistance.")
        
        return render(request, self.template_name, {'form': form})

def ai_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        openai.api_key = settings.OPENROUTER_API_KEY
        openai.base_url = "https://openrouter.ai/api/v1/"

        try:
            response = openai.chat.completions.create(
                model="meta-llama/llama-3-8b-instruct",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI Assistant dedicated to providing information strictly about Barangay-related topics only. "
                            "If the user's question is not related to the Barangay (such as technology, personal life, or entertainment), "
                            "politely respond with 'I'm here to assist with Barangay-related information only.'"
                        )
                    },
                    {"role": "user", "content": user_message}
                ]
            )

            ai_reply = response.choices[0].message.content

        except openai.OpenAIError as e:
            ai_reply = f"AI Error: {str(e)}"
        except Exception as e:
            ai_reply = f"Unexpected Error: {str(e)}"

        return JsonResponse({'response': ai_reply})

class ErrorPageView(TemplateView):
    template_name = 'error/page-not-authorized.html'