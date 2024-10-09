from django.db import models
from django.conf import settings


# Create your models here.
class Equipment(models.Model):
    CATEGORY_CHOICES = (
        ('tractor', 'Tractor'),
        ('harvester', 'Harvester'),
        ('plow', 'Plow')
        # To add more categories
    )
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('bookec', 'B')],
                              default='available')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
