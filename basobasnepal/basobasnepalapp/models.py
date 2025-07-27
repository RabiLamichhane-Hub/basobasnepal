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
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True)
    ward_num = models.BigIntegerField()
    street = models.CharField(max_length=50, null=True)
    num_of_rooms_available = models.BigIntegerField()
    contact_number = models.BigIntegerField()
    description = models.CharField(max_length=200)
    photos = models.ImageField(upload_to='room_photos/')

    def __str__(self):
        return f"{self.municipality.name},{self.ward_num}"