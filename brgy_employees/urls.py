from django.urls import path
from .views import (EmployeeDashboardView,
                    EmployeeManageReports,
                    EmployeeManageRequest,
                    EmployeeResolution,
                    EmployeeOrdinance,
                    EmployeeManageProgram,
                    EmployeeManageEquipment,
                    EmployeeManageSupplies,
                    ManageResidentList,
)

app_name = 'brgy_employees'

urlpatterns = [
    path('dashboard/', EmployeeDashboardView.as_view(), name='dashboard'),
    
    #pages for services
    path('Residents/', ManageResidentList.as_view(), name='residents_list'),
    path('incidents/', EmployeeManageReports.as_view(), name = 'incidents_reports'),
    path('Request/', EmployeeManageRequest.as_view(), name = 'resident_request'),
    
    #program
    path('Programs/', EmployeeManageProgram.as_view(), name = 'manage_programs'),
    
    #inventory
    path('Equipments/', EmployeeManageEquipment.as_view(), name = 'manage_equipments'),
    path('Supplies/', EmployeeManageSupplies.as_view(), name = 'manage_supplies'),
    
    
    #documents 
    path('Ordinance/', EmployeeOrdinance.as_view(), name = 'employee_ordinance'),
    path('Resolution/', EmployeeResolution.as_view(), name = 'employee_resolution'),
]
