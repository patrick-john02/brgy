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
)

app_name = 'social_service'

urlpatterns = [
    # Social Welfare
    path('welfare/', SocialWelfareApplicationListView.as_view(), name='social_welfare_applications'),
    path('welfare/apply/', SocialWelfareApplicationCreateView.as_view(), name='social_welfare_apply'),
    path('welfare/<int:pk>/', SocialWelfareApplicationDetailView.as_view(), name='application_detail'),
    
    # PWD/Senior
    path('pwd-senior/', PwdSeniorServiceRequestListView.as_view(), name='pwd_senior_requests'),
    path('pwd-senior/request/', PwdSeniorServiceRequestCreateView.as_view(), name='pwd_senior_request'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
