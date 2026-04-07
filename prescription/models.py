import uuid
from django.db import models

from medicine.models import Medicine
from treatment.models import Treatment

class Prescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    treatment = models.ForeignKey(Treatment, on_delete=models.PROTECT, related_name="prescriptions")
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name="medicine")
    instruction= models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['treatment', 'medicine'],
                name='unique_treatment_medicine'
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Prescription {self.id}"