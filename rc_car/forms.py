from django import forms
from datetime import datetime
from .models import RC_Car

class New_Car(forms.ModelForm):
    class Meta:
        model = RC_Car
        fields = ('name',)
