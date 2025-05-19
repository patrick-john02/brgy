from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from .views import (
    EmergencyContactListView, EmergencyContactCreateView,
    HealthIssueListView, HealthIssueCreateView,
    MedicalRequestListView, MedicalRequestCreateView,
    EmergencyContactUpdateView, EmergencyContactDeleteView,
    HealthIssueUpdateView, HealthIssueDeleteView,
    MedicalAssistanceRequestListView, MedicalAssistanceRequestCreateView,
    MedicalAssistanceRequestUpdateView, MedicalAssistanceRequestDeleteView,
    AdminEmergencyContactListViews,
)

app_name = 'health_emergency'

urlpatterns = [
    # path('contacts/', EmergencyContactListView.as_view(), name='emergency_contacts'),
    path('contacts/add/', EmergencyContactCreateView.as_view(), name='add_emergency_contact'),

    path('health-issues/', HealthIssueListView.as_view(), name='health_issues'),
    path('health-issues/report/', HealthIssueCreateView.as_view(), name='report_health_issue'),

    path('medical-requests/', MedicalRequestListView.as_view(), name='medical_requests'),
    path('medical-requests/new/', MedicalRequestCreateView.as_view(), name='request_medical_assistance'),

    #admin side urls
    path('admin/emergency-contacts/', AdminEmergencyContactListViews.as_view(), name='emergency_admin_contacts'),
    path('admin/emergency-contacts/create/', EmergencyContactCreateView.as_view(), name='create_emergency_contact'),
    path('admin/emergency-contacts/<int:pk>/update/', EmergencyContactUpdateView.as_view(), name='update_emergency_contact'),
    path('admin/emergency-contacts/<int:pk>/delete/', EmergencyContactDeleteView.as_view(), name='delete_emergency_contact'),

    # Admin and Employee views for Health Issues
    path('admin/health-issues/', HealthIssueListView.as_view(), name='health_issues'),
    path('admin/health-issues/create/', HealthIssueCreateView.as_view(), name='create_health_issue'),
    path('admin/health-issues/<int:pk>/update/', HealthIssueUpdateView.as_view(), name='update_health_issue'),
    path('admin/health-issues/<int:pk>/delete/', HealthIssueDeleteView.as_view(), name='delete_health_issue'),

    # Admin and Employee views for Medical Assistance Requests
    path('admin/medical-requests/', MedicalAssistanceRequestListView.as_view(), name='medical_requests'),
    path('admin/medical-requests/create/', MedicalAssistanceRequestCreateView.as_view(), name='create_medical_request'),
    path('admin/medical-requests/<int:pk>/update/', MedicalAssistanceRequestUpdateView.as_view(), name='update_medical_request'),
    path('admin/medical-requests/<int:pk>/delete/', MedicalAssistanceRequestDeleteView.as_view(), name='delete_medical_request'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)