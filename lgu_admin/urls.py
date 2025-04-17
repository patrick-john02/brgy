# lgu_admin/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .consumers import ChatConsumer
from .views import (AdminDashboardView, 
                    AdminResidentsList,
                    ArchiveResidentView,
                    UnarchiveResidentView,
                    ArchivedResidentsListView,
                    UnverifiedResidentsListView,
                    AdminResidentAccountList,
                    AdminAccountList,
                    DeleteUserView,
                    UserDetailView,
                    verify_resident,
                    AdminReportsView,
                    # ChatListView,
                    # ChatDetailView,
                    # SendMessageView,
                    AdminBarangayClearance,
                    AdminPendingRequestsView,
                    PrintCertificateView,
                    ApproveCertificationView,
                    AdminApprovedRequestsView,
                    AdminRejectedRequestsView,
                    AdminBarangayEquipment,
                    # AdminBarangaySupplies,
                    # AdminResolution,
                    # AdminOrdinance,
                    # AdminMemorandum,
                    AdminServicesView,
                    ServiceUpdateView,
                    ServiceDeleteView,
                    AdminProjectsView,
                    EditProjectView,
                    DeleteProjectView,
                    AdminOfficialsView,
                    CustomLogoutView,
                    AddResidentView,
                    ResidentDetailView,
                    EditEmployeeView,
                    DeleteOfficialView,
                    
                    InventoryCategoryView,
                    InventoryItemView,
                    InventoryItemUpdateView,
                    # InventoryTransactionView
                    AdminProfileView,       
                     
)
app_name = 'lgu_admin'

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),
    path('profile/', AdminProfileView.as_view(), name='profile'),
    
    #residents CRUD and ETL
    path('residents/', AdminResidentsList.as_view(), name='residents_list'),
    path('residents/add/', AddResidentView.as_view(), name='add_resident'),
    path('residents/<int:resident_id>/', ResidentDetailView.as_view(), name='resident_details'),
    path('residents/archived/', ArchivedResidentsListView.as_view(), name='archived_residents'),
    path('residents/archive/<int:resident_id>/', ArchiveResidentView.as_view(), name='archive_resident'),
    path('residents/unarchive/<int:resident_id>/', UnarchiveResidentView.as_view(), name='unarchive_resident'),
    
    path('unverified-residents/', UnverifiedResidentsListView.as_view(), name='unverified_residents'),
    path('resident-accounts/', AdminResidentAccountList.as_view(), name='resident_account_list'),

    #for employee accounts
    path('acounts/', AdminAccountList.as_view(), name='account_list'),
    path("accounts/edit/<int:pk>/", EditEmployeeView.as_view(), name="edit_user"),
    path('view-user/<int:pk>/', UserDetailView.as_view(), name='view_user'),
    path('verify-resident/<int:pk>/', verify_resident, name='verify_resident'),
    path("delete_user/<int:user_id>/", DeleteUserView.as_view(), name="delete_user"),
    
    path("reports/", AdminReportsView.as_view(), name="reports"),
    # path("", ChatListView.as_view(), name="chat-list"),
    # path("thread/<int:thread_id>/", ChatDetailView.as_view(), name="chat-detail"),
    # path("<int:user_id>/send/", SendMessageView.as_view(), name="send-message"),

    
    path('clearance/', AdminBarangayClearance.as_view(), name='brgy_clearance'),
    path('pending-requests/', AdminPendingRequestsView.as_view(), name='admin_pending_requests'),
    path('print-certificate/<str:document_type>/<int:request_id>/', PrintCertificateView.as_view(), name='print_certificate'),
    path('approve/<int:request_id>/', ApproveCertificationView.as_view(), name='approve_certificate'),
    
    path('approved-requests/', AdminApprovedRequestsView.as_view(), name='admin_approved_requests'),
    path('rejected-requests/', AdminRejectedRequestsView.as_view(), name='admin_rejected_requests'),
    
    # path('supplies/', AdminBarangaySupplies.as_view(), name='brgy_supplies'),
    # path('resolution', AdminResolution.as_view(), name='resolution'),
    # path('ordinance/', AdminOrdinance.as_view(), name='ordinances'),
    # path('memorandum/', AdminMemorandum.as_view(), name='memorandums'),
    
    
    path('services/', AdminServicesView.as_view(), name='service'),
    path('update-service/<int:pk>/', ServiceUpdateView.as_view(), name='update_service'),
    path('delete-service/<int:pk>/', ServiceDeleteView.as_view(), name='delete_service'),


    path('projects/', AdminProjectsView.as_view(), name='project'),
    path('projects/edit/<int:project_id>/', EditProjectView.as_view(), name='edit_project'),
    path('projects/delete/<int:project_id>/', DeleteProjectView.as_view(), name='delete_project'),
    
    path('officials/', AdminOfficialsView.as_view(), name='official'),
    path('delete_official/', DeleteOfficialView.as_view(), name='delete_official'),

    
    
    path('inventory/categories/', InventoryCategoryView.as_view(), name='inventory_categories'),
    path('inventory/items/', InventoryItemView.as_view(), name='inventory_items'),
    path('inventory/items/<int:item_id>/update/', InventoryItemUpdateView.as_view(), name='update_inventory_item'),
    path('equipment/', AdminBarangayEquipment.as_view(), name='brgy_equipment'),
    # path('inventory/transactions/', InventoryTransactionView.as_view(), name='inventory_transactions'),
    
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
websocket_urlpatterns = [
    path("ws/chat/<int:thread_id>/", ChatConsumer.as_asgi()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)