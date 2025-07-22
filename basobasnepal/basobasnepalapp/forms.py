from django import forms
from .models import Room, Province, District, Municipality

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
