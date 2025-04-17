from django.db import models
from core.models import CustomUser
from core.models import CustomUser

class BarangayAdmin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="barangay_admin")
    position = models.CharField(max_length=100, default="Barangay Admin")
    date_assigned = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.position}"

class BarangayReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('complaint', 'Complaint'),
        ('incident', 'Incident'),
        ('accident', 'Accident'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='lgu_admin/reports/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.name} - {self.report_type} - {self.date_created}"
    
class ChatThread(models.Model):

    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="chat_threads_initiated")
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="chat_threads_received")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"

    @classmethod
    def get_or_create_thread(cls, user1, user2):
        if user1 == user2:
            raise ValueError("Users cannot chat with themselves!")
    
        thread, created = cls.objects.get_or_create(
            user1=min(user1, user2, key=lambda x: x.id),
            user2=max(user1, user2, key=lambda x: x.id),
        )
        return thread, created


class Message(models.Model):
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField(blank=True, null=True) 
    file = models.FileField(upload_to="chat_files/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_report = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.sender not in [self.thread.user1, self.thread.user2] or self.receiver not in [self.thread.user1, self.thread.user2]:
            raise ValueError("Sender and receiver must be part of the chat thread!")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.content[:30]}..."
    
    
    

class InventoryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=50, default='pcs')
    critical_level = models.PositiveIntegerField(default=5)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def is_below_critical(self):
        return self.quantity < self.critical_level

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]

    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    remarks = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    handled_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.item.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        if self.transaction_type == 'IN':
            self.item.quantity += self.quantity
        elif self.transaction_type == 'OUT':
            if self.item.quantity >= self.quantity:
                self.item.quantity -= self.quantity
            else:
                raise ValueError("Cannot remove more items than in stock.")
        self.item.save()
        super().save(*args, **kwargs)