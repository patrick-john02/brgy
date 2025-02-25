from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib import messages


class CustomLoginView(LoginView):
    template_name = 'core/login.html'

    def get_redirect_url(self):
        """Get the URL to redirect to after login based on user type."""
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


class LandingPageView(TemplateView):
    template_name = 'core/landingpage.html'

class ErrorPageView(TemplateView):
    template_name = 'error/page-not-authorized.html'
