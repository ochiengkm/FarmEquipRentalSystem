from django.db import models
from equipment.models import Equipment
from renters.models import Renters


class Bookings(models.Model):
    id = models.AutoField(primary_key=True)
    renters = models.ForeignKey(Renters, on_delete=models.CASCADE)
    # Remove the 'to_field' to reference the primary key (id) of Equipment
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    reservationDate = models.DateTimeField(auto_now_add=True)
    pickupDate = models.DateField()

    def __str__(self):
        return f"{self.renters.email} - {self.equipment.name}"

    class Meta:
        db_table = 'bookings'
        constraints = [
            models.UniqueConstraint(fields=['renters', 'equipment'], name='unique_renter_equipment_booking')
        ]
