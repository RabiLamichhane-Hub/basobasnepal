from django import forms
from . models import Room, Municipality, District, Province

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = 'province', 'district','municipality', 'ward_num','street', 'num_of_rooms_available', 'contact_number', 'description', 'photos'

class LocationFilterForm(forms.Form):
    province = forms.ModelChoiceField(queryset=Province.objects.all(), required=True)
    district = forms.ModelChoiceField(queryset=District.objects.none(), required=True)
    municipality = forms.ModelChoiceField(queryset=Municipality.objects.none(), required=True)
