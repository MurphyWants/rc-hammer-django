from django.shortcuts import render, redirect

from .models import RC_Car

# Create your views here.


def index(request):
    template_name = 'dashboard/index.html'

    if request.user == False:
        redirect('Home.views.index')

    current_user = request.user
    cars_owned = RC_Car.objects.filter(owner__id=current_user.id)
    cars_can_drive = RC_Car.objects.filter(user_list__id=current_user.id)
    cars_watch = RC_Car.objects.filter(viewer_list__id=current_user.id) | RC_Car.objects.filter(user_list__id=current_user.id)
    return render(request, template_name, {'rc_car_owned_list' : cars_owned,
                                            'rc_car_shared_list': cars_watch,
                                            'rc_car_can_drive_list' : cars_can_drive})


def by_uuid(request, unique_id):
    template_name = 'rc/by_uuid.html'
    try:
        rc_car = RC_Car.objects.get(pk=unique_id)
    except RC_Car.DoesNotExist:
        return redirect(request.get_full_path())

    current_user = request.user
    car_owner = rc_car.owner

    if (current_user.id == car_owner.id):
        return render(request, template_name, {'rc' : rc_car, 'car_owner' : True})

    if (current_user in rc_car.user_list.all()):
        return render(request, template_name, {'rc' : rc_car, 'car_user' : True})

    if (current_user in rc_car.viewer_list.all()):
        return render(request, template_name, {'rc' : rc_car, 'car_viewer' : True})

    return redirect(request.get_full_path())
