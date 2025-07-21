from django import forms
from . models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = 'province', 'district','municipality', 'ward_num','street', 'num_of_rooms_available', 'contact_number', 'description', 'photos'