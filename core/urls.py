from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.urls import path
from .views import CustomLoginView, LandingPageView, ErrorPageView, ResidentRegistrationView

app_name = 'core'

urlpatterns = [
    #landing page
    path('', LandingPageView.as_view(), name='landing'),
    
    path('chat/', TemplateView.as_view(template_name="core/chat.html"), name='chat'),

    #login page
    path('login/', CustomLoginView.as_view(), name='login'),
    
    path('register/resident/', ResidentRegistrationView.as_view(), name='resident_registration'),
    
    #error page
    path('Error/', ErrorPageView.as_view(), name='error'),
path('forgot-password/', auth_views.PasswordResetView.as_view(
    template_name='core/forgot_password.html',
    email_template_name='core/password_reset_email.html',
    subject_template_name='core/password_reset_subject.txt',
    success_url=reverse_lazy('core:password_reset_done')
), name='forgot_password'),


path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(
    template_name='core/password_reset_done.html'
), name='password_reset_done'),

path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='core/password_reset_confirm.html',
    success_url=reverse_lazy('core:password_reset_complete')
), name='password_reset_confirm'),

path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
    template_name='core/password_reset_complete.html'
), name='password_reset_complete'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)