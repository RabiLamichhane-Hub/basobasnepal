from django.db import models
from django.contrib.auth.models import User


class Province(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Municipality(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



# Create your models here.
class Room(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    province = models.CharField(max_length=15)
    district = models.CharField(max_length=15, null=False)
    municipality = models.CharField(max_length=20, null=False)
    ward_num = models.IntegerField()
    street = models.CharField(max_length=50, null=True)
    num_of_rooms_available = models.IntegerField()
    contact_number = models.IntegerField()
    description = models.CharField(max_length=200)
    
    photos = models.ImageField(upload_to='room_photos/')

    def __str__(self):
        return (self.municipality)