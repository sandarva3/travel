from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=45)
    age = models.IntegerField(default=20)
    nationality = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, default='m')
    

    def __str__(self):
        return self.username #Calling str() method of super().
    

