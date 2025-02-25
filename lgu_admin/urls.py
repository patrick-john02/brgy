# lgu_admin/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (AdminDashboardView, 
                    AdminResidentsList,
                    AdminAccountList,
                    AdminReports,
                    AdminBarangayClearance,
                    AdminBarangayEquipment,
                    AdminBarangaySupplies,
                    AdminResolution,
                    AdminOrdinance,
                    AdminMemorandum,
                    AdminServicesView,
                    AdminProjectsView,
                    AdminOfficialsView,
                    CustomLogoutView,
                    AddResidentView,
                    ResidentDetailView,
                    
)
                    

app_name = 'lgu_admin'

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),
    
    #residents CRUD and ETL
    path('residents/', AdminResidentsList.as_view(), name='residents_list'),
    path('residents/add/', AddResidentView.as_view(), name='add_resident'),
    path('residents/<int:resident_id>/', ResidentDetailView.as_view(), name='resident_details'),

    path('acounts/', AdminAccountList.as_view(), name='account_list'),
    path('reports/', AdminReports.as_view(), name='reports'),
    path('clearance/', AdminBarangayClearance.as_view(), name='brgy_clearance'),
    path('equipment/', AdminBarangayEquipment.as_view(), name='brgy_equipment'),
    path('supplies/', AdminBarangaySupplies.as_view(), name='brgy_supplies'),
    path('resolution', AdminResolution.as_view(), name='resolution'),
    path('ordinance/', AdminOrdinance.as_view(), name='ordinances'),
    path('memorandum/', AdminMemorandum.as_view(), name='memorandums'),
    path('services/', AdminServicesView.as_view(), name='service'),
    path('projects/', AdminProjectsView.as_view(), name = 'project'),
    path('officials/', AdminOfficialsView.as_view(), name='official'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)