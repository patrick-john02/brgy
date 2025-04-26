from django.contrib import admin
from .models import (
    BarangayReport, 
    ChatThread, 
    Message, 
    BarangayAdmin, 
    InventoryCategory, 
    InventoryItem, 
    InventoryTransaction
)
admin.site.register(BarangayAdmin)
admin.site.register(BarangayReport)
admin.site.register(InventoryCategory)
admin.site.register(InventoryItem)
admin.site.register(InventoryTransaction)
# admin.site.register(ChatThread)
# admin.site.register(Message)
