from django.shortcuts import render

from .models import RC_Car

# Create your views here.


def index(request):
    template_name = 'dashboard/index.html'
    current_user = request.user
    cars_owned = RC_Car.objects.filter(owner__id=current_user.id)
    cars_shared = RC_Car.objects.filter(viewer_list__id=current_user.id) | RC_Car.objects.filter(user_list__id=current_user.id)
    return render(request, template_name, {'rc_car_owned_list' : cars_owned,
                                            'rc_car_shared_list': cars_shared})


def by_uuid(request, unique_id):
    return 0
