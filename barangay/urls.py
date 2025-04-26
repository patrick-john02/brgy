"""
URL configuration for barangay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('lgu_admin/', include('lgu_admin.urls', namespace='lgu_admin')),
    path('brgy_employees/', include('brgy_employees.urls', namespace='brgy_employees')),
    path('residents/', include('residents.urls' , namespace='residents')),
    path('SocialServiceandWelfare/', include('SocialServicesAndWelfare.urls' , namespace='social_service')),
    path('CommunityandEventManagement/', include('CommunityAndEventManagement.urls' , namespace='community_event')),
    path('EducationandTraining/', include('EducationAndTraining.urls' , namespace='education_training')),
    path('BarangayNewsandUpdates/', include('BarangayNewsAndUpdates.urls' , namespace='barangay_news')),
    path('HealthandEmergencyServices/', include('HealthAndEmergencyServices.urls' , namespace='health_emergency')),
    # path("chat/", include("chat.urls")), HealthAndEmergencyServices
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)