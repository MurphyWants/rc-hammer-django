from django.apps import AppConfig

class RcCarConfig(AppConfig):
    name = 'rc_car'

    """def ready(self):
        from .models import RC_Car
        for car in RC_Car.objects.all():
            car.current_user = None
            car.save()"""
