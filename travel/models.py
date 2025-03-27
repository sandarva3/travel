from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=45)
    age = models.IntegerField(default=20)
    nationality = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, default='m')

    def __str__(self):
        return self.username #Calling str() method of super().


class Place(models.Model):
    name = models.CharField(max_length=70)
    place_id = models.CharField(max_length=27, default="fakeId")
    full_address = models.CharField(max_length=300)
    coordinates = models.JSONField(default=dict)
    summary = models.TextField()
    mainstream = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['place_id'], name='place_id_idx'),
        ]

    def __str__(self):
        return self.name