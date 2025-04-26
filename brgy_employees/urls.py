from django.urls import path
from .views import (EmployeeDashboardView,
                    EmployeeManageReports,
                    EmployeeManageRequest,
                    EmployeeManageProgram,
                    EmployeeManageEquipment,
                    EmployeeManageSupplies,
                    ManageResidentList,
                    
                    AddResidentView,
                    ResidentDetailView,
                    ArchivedResidentsListView,
                    ArchiveResidentView,
                    UnarchiveResidentView,
                    
                    EmployeeBarangayClearance,
                    EmployeePendingRequestsView,
                    PrintCertificateView,
                    ApproveCertificationView,
                    EmployeeApprovedRequestsView,
                    EmployeeRejectedRequestsView,
                    
                    
)

app_name = 'brgy_employees'

urlpatterns = [
    path('dashboard/', EmployeeDashboardView.as_view(), name='dashboard'),
    
    #pages for services

    path('incidents/', EmployeeManageReports.as_view(), name = 'incidents_reports'),
    path('Request/', EmployeeManageRequest.as_view(), name = 'resident_request'),
    
    #residents details and informations
    path('residents/add/', AddResidentView.as_view(), name='add_resident'),
    path('Residents/', ManageResidentList.as_view(), name='residents_list'),
    path('residents/<int:resident_id>/', ResidentDetailView.as_view(), name='resident_details'),
    path('residents/archived/', ArchivedResidentsListView.as_view(), name='archived_residents'),
    path('residents/archive/<int:resident_id>/', ArchiveResidentView.as_view(), name='archive_resident'),
    path('residents/unarchive/<int:resident_id>/', UnarchiveResidentView.as_view(), name='unarchive_resident'),
    
    
    #barangay documents
    path('clearance/', EmployeeBarangayClearance.as_view(), name='brgy_clearance'),
    path('pending-requests/', EmployeePendingRequestsView.as_view(), name='employee_pending_requests'),
    path('print-certificate/<str:document_type>/<int:request_id>/', PrintCertificateView.as_view(), name='print_certificate'),
    path('approve/<int:request_id>/', ApproveCertificationView.as_view(), name='approve_certificate'),
    
    path('approved-requests/', EmployeeApprovedRequestsView.as_view(), name='admin_approved_requests'),
    path('rejected-requests/', EmployeeRejectedRequestsView.as_view(), name='admin_rejected_requests'),
    
    #program
    path('Programs/', EmployeeManageProgram.as_view(), name = 'manage_programs'),
    
    #inventory
    path('Equipments/', EmployeeManageEquipment.as_view(), name = 'manage_equipments'),
    path('Supplies/', EmployeeManageSupplies.as_view(), name = 'manage_supplies'),
    
    
]
