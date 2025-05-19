from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    SocialWelfareApplicationListView,
    PwdSeniorServiceRequestListView,
    PwdSeniorServiceRequestCreateView,
    SocialWelfareApplicationCreateView,
    SocialWelfareApplicationDetailView,
    
    SocialWelfareApplicationAdminListView, SocialWelfareApplicationAdminDetailView,
    SocialWelfareApplicationAdminUpdateView, PwdSeniorServiceRequestAdminListView,
    PwdSeniorServiceRequestAdminDetailView, PwdSeniorServiceRequestAdminUpdateView,
    SocialWelfareApplicationDeleteView, SocialWelfareApplicationApproveView
)

app_name = 'social_service'

urlpatterns = [
    # Social Welfare
    path('welfare/', SocialWelfareApplicationListView.as_view(), name='social_welfare_applications'),
    path('welfare/apply/', SocialWelfareApplicationCreateView.as_view(), name='social_welfare_apply'),
    path('welfare/<int:pk>/', SocialWelfareApplicationDetailView.as_view(), name='application_detail_user'),
    
    # PWD/Senior
    path('pwd-senior/', PwdSeniorServiceRequestListView.as_view(), name='pwd_senior_requests'),
    path('pwd-senior/request/', PwdSeniorServiceRequestCreateView.as_view(), name='pwd_senior_request'),
    
    path('admin/social-welfare/', SocialWelfareApplicationAdminListView.as_view(), name='social_welfare_admin_list'),
    path('admin/social-welfare/<int:pk>/', SocialWelfareApplicationAdminDetailView.as_view(), name='application_detail'),
    path('admin/social-welfare/update/<int:pk>/', SocialWelfareApplicationAdminUpdateView.as_view(), name='application_update'),
    path('welfare/detail/<int:pk>/', SocialWelfareApplicationAdminDetailView.as_view(), name='social_welfare_application_detail'),
    path('welfare/delete/<int:pk>/', SocialWelfareApplicationDeleteView.as_view(), name='delete_social_welfare_application'),
    path('welfare/approve/<int:pk>/', SocialWelfareApplicationApproveView.as_view(), name='approve_social_welfare_application'),
    
    
    # Admin views for PWD/Senior Service Requests
    path('admin/pwd-senior/', PwdSeniorServiceRequestAdminListView.as_view(), name='pwd_senior_admin_list'),
    path('admin/pwd-senior/<int:pk>/', PwdSeniorServiceRequestAdminDetailView.as_view(), name='pwd_senior_request_detail'),
    path('admin/pwd-senior/update/<int:pk>/', PwdSeniorServiceRequestAdminUpdateView.as_view(), name='pwd_senior_request_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
