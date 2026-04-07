import uuid
from django.db import models

class Treatment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.UUIDField(db_index=True)    
    reservation = models.UUIDField(db_index=True)
    diagnosis = models.TextField(null=True, blank=True)
    action_take = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.UUIDField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Treatment {self.id}"