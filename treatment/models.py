import uuid
from django.db import models

class Treatment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.UUIDField(db_index=True)    
    reservation_id = models.UUIDField(db_index=True)
    diagnosis = models.TextField(null=True, blank=True)
    action_take = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_by = models.UUIDField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Treatment {self.id}"