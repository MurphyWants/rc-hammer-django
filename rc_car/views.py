from django.shortcuts import render

from .models import RC_Car

# Create your views here.


def index(request):
    template_name = 'dashboard/index.html'
    current_user = request.user
    cars = RC_Car.objects.filter(owner__id=current_user)
    return render(request, template_name, {'rc_car_user_list' : cars})


def by_uuid(request, unique_id):
    return 0
