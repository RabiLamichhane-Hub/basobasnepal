from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    location_district = models.CharField(max_length=15, null=False)
    location_municipality = models.CharField(max_length=20, null=False)
    location_ward_num = models.IntegerField()
    num_of_rooms_available = models.IntegerField()
    contact_number = models.IntegerField()
    description = models.CharField(max_length=200)
    
    photos = models.ImageField(upload_to='room_photos/')

    def __str__(self):
        return (self.location_municipality)