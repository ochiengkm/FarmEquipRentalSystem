from django.db import models


# Create your models here.
class OTP(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    email = models.TextField()
    otp = models.TextField()
    expirydate = models.TextField()


    def __str__(self):
        return f"{self.id} - {self.email}"

    class Meta:
        db_table = 'otps'
