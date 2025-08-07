from django import forms
from .models import Room, Province, District, Municipality, Booking

class RoomForm(forms.ModelForm):
    province = forms.ModelChoiceField(queryset=Province.objects.all(), required=True)
    district = forms.ModelChoiceField(queryset=District.objects.none(), required=True)
    municipality = forms.ModelChoiceField(queryset=Municipality.objects.none(), required=True)

    class Meta:
        model = Room
        # Exclude owner because it's set in the view
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Handle POST data to filter queryset dynamically
        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['district'].queryset = District.objects.filter(province_id=province_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['district'].queryset = District.objects.none()
        elif self.instance.pk and self.instance.province:
            self.fields['district'].queryset = District.objects.filter(province=self.instance.province)

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['municipality'].queryset = Municipality.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['municipality'].queryset = Municipality.objects.none()
        elif self.instance.pk and self.instance.district:
            self.fields['municipality'].queryset = Municipality.objects.filter(district=self.instance.district)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'contact', 'adults', 'children', 'parmanent_address', 'occupation', 'additional_info']

        # Add this 'labels' dictionary to customize the text for each field
        labels = {
            'name': 'Your Full Name',
            'contact': 'Contact Number',
            'adults': 'Number of Adults',
            'children': 'Number of Children',
            'parmanent_address': 'Permanent Address',
            'occupation': 'Your Occupation',
            'additional_info': 'Additional Information',
        }

        # BONUS: You can also add placeholders and other HTML attributes using widgets
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Jane Doe'}),
            'contact': forms.TextInput(attrs={'placeholder': 'e.g., 98xxxxxxxx'}),
            'parmanent_address': forms.TextInput(attrs={'placeholder': 'City, Street, House No.'}),
            'occupation': forms.TextInput(attrs={'placeholder': 'e.g., Student, Engineer'}),
            'additional_info': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Any special requests or notes...'}),
        }