from django.db import models


# Create your models here.

class Renters(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'renters'
