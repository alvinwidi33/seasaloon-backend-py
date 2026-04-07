import uuid
from django.db import models

from medicine.models import Medicine
from treatment.models import Treatment

class Prescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    treatment_id = models.ForeignKey(Treatment, on_delete=models.PROTECT)
    medicine_id = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    instruction= models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription {self.id}"