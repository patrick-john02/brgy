# lgu_admin/management/commands/seed_inventory.py

from django.core.management.base import BaseCommand
from lgu_admin.models import InventoryCategory, InventoryItem


class Command(BaseCommand):
    help = 'Seed inventory with sample categories and items'

    def handle(self, *args, **kwargs):
        # Create or get categories
        electronics, _ = InventoryCategory.objects.get_or_create(
            name="Electronics", defaults={"description": "Electronic devices and gadgets"}
        )
        furniture, _ = InventoryCategory.objects.get_or_create(
            name="Furniture", defaults={"description": "Office and home furniture"}
        )
        stationery, _ = InventoryCategory.objects.get_or_create(
            name="Stationery", defaults={"description": "Office and school supplies"}
        )

        # Create sample items
        InventoryItem.objects.get_or_create(
            name="Laptop",
            defaults={
                "description": "Dell Inspiron 15",
                "category": electronics,
                "quantity": 10,
                "unit": "pcs",
                "critical_level": 3
            }
        )

        InventoryItem.objects.get_or_create(
            name="Office Chair",
            defaults={
                "description": "Ergonomic chair with lumbar support",
                "category": furniture,
                "quantity": 5,
                "unit": "pcs",
                "critical_level": 2
            }
        )

        InventoryItem.objects.get_or_create(
            name="Ballpen",
            defaults={
                "description": "Blue ink pens",
                "category": stationery,
                "quantity": 100,
                "unit": "pcs",
                "critical_level": 20
            }
        )

        self.stdout.write(self.style.SUCCESS('✅ Sample inventory data added successfully.'))
