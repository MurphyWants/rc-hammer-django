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

class Edit_Car(forms.ModelForm):

    class Meta:
        model = RC_Car
        fields = ('name', 'public_watch', 'public_drive')
        exclude = ('date_added', 'last_used', 'id', 'viewer_list', 'user_list', 'owner')

    def save(self, commit=True):
        car = super(New_Car, self).save(commit=False)
        car.name = self.cleaned_data['name']

        if commit:
            car.save()

        return car

    def __init__(self, *args, **kwargs):
        '''
        https://stackoverflow.com/questions/22847281/setting-initial-values-in-form-meta-class
        '''
        initial = kwargs.get('initial', {})
        initial['name'] = 'initial_name'
        kwargs['initial'] = initial
        super(Edit_Car, self).__init__(*args, **kwargs)
