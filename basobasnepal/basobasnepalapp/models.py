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
    ward_num = models.PositiveBigIntegerField()
    street = models.CharField(max_length=50, null=True)
    num_of_rooms_available = models.PositiveBigIntegerField()
    contact_number = models.PositiveBigIntegerField()
    description = models.CharField(max_length=200)
    photos = models.ImageField(upload_to='room_photos/')
    availbility = models.BooleanField(default=True)
    approve = models.BooleanField(default= False)

    def __str__(self):
        return f"{self.municipality.name},{self.ward_num}"
    
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    applicant_name = models.CharField(null=False)
    contact = models.PositiveBigIntegerField(null=False)
    adults = models.PositiveIntegerField(null=False)
    children = models.PositiveIntegerField(default=0)
    parmanent_address = models.CharField(max_length=50, null=False)
    occupation = models.CharField(max_length=20, null=False)
    additional_info = models.TextField(blank=True)
    date_requested = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking by {self.user.username} of Room {self.room.id}"