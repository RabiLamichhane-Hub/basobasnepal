from django import forms
from . models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = 'location_district', 'location_district', 'location_ward_num', 'num_of_rooms_available', 'contact_number', 'description', 'photos'