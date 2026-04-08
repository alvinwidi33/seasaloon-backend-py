import uuid
from django.db import models

from medicine.models import Medicine
from treatment.models import Treatment

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    reservation_id = models.UUIDField()

    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id}"
    
class InvoiceItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="items"
    )

    treatment = models.ForeignKey(
        Treatment,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    medicine = models.ForeignKey(
        Medicine,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.id}"