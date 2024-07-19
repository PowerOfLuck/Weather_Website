from django.db import models

class UserCity(models.Model):
    session_key = models.CharField(max_length=255, unique=True)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
