from .models import RC_Car
from rest_framework import serializers

class Rc_Car_Serializer(serializers.ModelSerializer):
    class Meta:
        model = RC_Car
        exclude = ('password', 'current_user')
