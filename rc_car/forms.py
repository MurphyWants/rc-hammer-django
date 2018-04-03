from django import forms
from datetime import datetime
from .models import RC_Car

class New_Car(forms.Form):
    name = forms.CharField(required=True, max_length=200, strip=True).help_text = '<br/>Name your car!'

    class Meta:
        model = RC_Car
        fields = ('name')

    def save(self, commit = True):
        car = super(New_Car, self).save(commit=False)
        car.name = self.cleaned_data['name']

        if commit:
            user.save()

        return car
