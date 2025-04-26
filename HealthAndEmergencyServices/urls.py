from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from .views import (
    EmergencyContactListView, EmergencyContactCreateView,
    HealthIssueListView, HealthIssueCreateView,
    MedicalRequestListView, MedicalRequestCreateView,
)

app_name = 'health_emergency'

urlpatterns = [
    path('contacts/', EmergencyContactListView.as_view(), name='emergency_contacts'),
    path('contacts/add/', EmergencyContactCreateView.as_view(), name='add_emergency_contact'),

    path('health-issues/', HealthIssueListView.as_view(), name='health_issues'),
    path('health-issues/report/', HealthIssueCreateView.as_view(), name='report_health_issue'),

    path('medical-requests/', MedicalRequestListView.as_view(), name='medical_requests'),
    path('medical-requests/new/', MedicalRequestCreateView.as_view(), name='request_medical_assistance'),

   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)