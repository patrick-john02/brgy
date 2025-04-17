from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.urls import path
from .views import CustomLoginView, LandingPageView, ErrorPageView, ResidentRegistrationView, ai_response

app_name = 'core'

urlpatterns = [
    #landing page
    path('', LandingPageView.as_view(), name='landing'),
    
    path('ai-response/', ai_response, name='ai_response'),
    path('chat/', TemplateView.as_view(template_name="core/chat.html"), name='chat'),

    #login page
    path('login/', CustomLoginView.as_view(), name='login'),
    
    path('register/resident/', ResidentRegistrationView.as_view(), name='resident_registration'),
    
    #error page
    path('Error/', ErrorPageView.as_view(), name='error'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)