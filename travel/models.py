from django.contrib.gis.db import models
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
    location = models.PointField(srid=4326)
    summary = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['location'], name='location_gist_idx'),  # Spatial index
        ]

    def __str__(self):
        return self.name