from django import forms
from django.contrib.auth import get_user_model
from ngos.models import NGO

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    phone = forms.CharField(max_length=17, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    
    # NGO specific fields
    organization_name = forms.CharField(max_length=150, required=False)
    capacity_kg = forms.FloatField(required=False, initial=50.0, help_text="Amount of food you can accept (if NGO)")
    latitude = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'id': 'id_latitude'}))
    longitude = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'id': 'id_longitude'}))
    
    # User-facing location strings for Map API if we were to use it
    location_string = forms.CharField(label="Location Address", required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter your address'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'phone', 'address']

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        if role == 'NGO':
            if not cleaned_data.get('organization_name'):
                self.add_error('organization_name', 'NGO Name is required.')
            if cleaned_data.get('latitude') is None or cleaned_data.get('longitude') is None:
                self.add_error('location_string', 'Please provide or allow location fetch for NGO matching.')
        return cleaned_data
