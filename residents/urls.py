from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (ResidentDashboardView, 
                    ResidentsDocumentRequest,
                    PendingRequestsView,
                    ApproveRequestsView,
                    RejectedRequestsView,
                    ResidentUploadIDView,
                    CustomLogoutView,
                    ResidentDocumentSubmitted,
                    ResidentDocumentApplyPrograms,
                    InventoryBorrow,
                    ResidentsProfileView,
                    PublicAnnouncementsView
)


app_name = 'residents'

urlpatterns = [
    path('dashboard/', ResidentDashboardView.as_view(), name='dashboard'),
    path('profile/', ResidentsProfileView.as_view(), name='profile'),

    #upload for verrifications
    path('upload-id/', ResidentUploadIDView.as_view(), name='resident_upload_id'),
    
    #documents paths
    path('documents/', ResidentsDocumentRequest.as_view(), name ='residendocument'),
    path('pending_requests/', PendingRequestsView.as_view(), name='pending_requests'),
    path('approve_requests/', ApproveRequestsView.as_view(), name='approve_requests'),
    path('reject_requests/', RejectedRequestsView.as_view(), name='reject_requests'),


    
    
    path('Submitted/', ResidentDocumentSubmitted.as_view(), name='barangay_submitted'),
    path('Programs/', ResidentDocumentApplyPrograms.as_view(), name='apply_programs'),
    path('inventory_borrow', InventoryBorrow.as_view(), name='inventory_borrow'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    
    path('public/announcements/', PublicAnnouncementsView.as_view(), name='public_announcements'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

