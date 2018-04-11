from django import forms
from datetime import datetime
from .models import RC_Car

class New_Car(forms.ModelForm):

    class Meta:
        model = RC_Car
        fields = ('name', 'password')
        exclude = ('owner','username')
        help_texts = {
            'password': "Create a password to authenticate your Car!",
            }
        widgets = {
            'name': forms.TextInput(),
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        car = super(New_Car, self).save(commit=False)
        car.name = self.cleaned_data['name']

        car.set_password(password)

        if commit:
            car.save()

        return car

class Edit_Car(forms.ModelForm):

    class Meta:
        model = RC_Car
        fields = ('name', 'public_watch', 'public_drive', 'user_list', 'viewer_list', 'owner')
        exclude = ('date_added', 'last_used', 'id')
        help_texts = {
            'owner': 'This changes who has ownership over the car. Be sure you really want to do this.',
        }

    def save(self, commit=True):
        car = super(Edit_Car, self).save(commit=False)
        car.name = self.cleaned_data['name']
        car.name = self.cleaned_data['password']

        if commit:
            car.save()

        return car
