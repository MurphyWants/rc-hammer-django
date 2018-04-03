from django import forms
from datetime import datetime
from .models import RC_Car

class New_Car(forms.Form):
    class Meta:
        model = RC_Car
        fields = ('name')

    def save(self, commit = True):
        car = super(New_Car, self).save(commit=False)
        car.name = self.cleaned_data['name']

        if commit:
            user.save()

        return car
