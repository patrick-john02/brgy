from django.urls import path
from .views import (ResidentDashboardView, 
                    # RequestBarangayClearance,
                    CustomLogoutView,
                    ResidentDocumentSubmitted,
                    ResidentDocumentApplyPrograms,
                    InventoryBorrow,
)


app_name = 'residents'

urlpatterns = [
    path('dashboard/', ResidentDashboardView.as_view(), name='dashboard'),
    # path('barangay_clearance/', RequestBarangayClearance.as_view(), name = 'barangay_clearance'),
    path('Submitted/', ResidentDocumentSubmitted.as_view(), name = 'barangay_submitted' ),
    path('Programs/', ResidentDocumentApplyPrograms.as_view(), name = 'apply_programs' ),
    # path('View_Programs/', RequestBarangayClearance.as_view(), name = 'view_programs'),
    path('inventory_borrow', InventoryBorrow.as_view(), name = 'inventory_borrow' ),
    
    
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
