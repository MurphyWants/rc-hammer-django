from django.apps import AppConfig
from .models import RC_Car

class RcCarConfig(AppConfig):
    name = 'rc_car'

    def ready(self):
        for car in RC_Car.objects.all():
            car.current_user = None
            print(car.id, " setting to None")
            car.save()
