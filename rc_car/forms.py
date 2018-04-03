from django import forms
from datetime import datetime
from .models import RC_Car

class New_Car(forms.ModelForm):
    name = forms.CharField(max_length=200, strip=True, min_length=1)

    class Meta:
        model = RC_Car
        fields = ('name',)
        exclude = ('owner',)

    def save(self, commit=True):
        car = super(New_Car, self).save(commit=False)
        car.name = self.cleaned_data['name']

        if commit:
            car.save()

        return car
