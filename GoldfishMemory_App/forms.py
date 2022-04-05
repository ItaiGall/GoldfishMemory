from django import forms
from .models import ParkingSpot

class SaveParkingSpotForm(forms.ModelForm):
    class Meta:
        model = ParkingSpot
        fields = '__all__'