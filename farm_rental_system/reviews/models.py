from django.db import models
from django.conf import settings
from equipment.models import Equipment


# Create your models here.
class Review(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.equipment.name} by {self.reviewer.username}"
