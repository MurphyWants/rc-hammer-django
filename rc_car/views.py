from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import New_Car as New_Car_Form, Edit_Car
from .models import RC_Car
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

@login_required(login_url="/login")
def index(request):
    template_name = 'dashboard/index.html'

    current_user = request.user
    cars_owned = RC_Car.objects.filter(owner__id=current_user.id)
    cars_can_drive = RC_Car.objects.filter(user_list__id=current_user.id)
    cars_watch = RC_Car.objects.filter(viewer_list__id=current_user.id) | RC_Car.objects.filter(user_list__id=current_user.id)
    return render(request, template_name, {'rc_car_owned_list' : cars_owned,
                                            'rc_car_shared_list': cars_watch,
                                            'rc_car_can_drive_list' : cars_can_drive})

@login_required(login_url="/login")
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

@login_required(login_url="/login")
def new_car(request):
    if request.method == 'POST':
        form = New_Car_Form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return HttpResponseRedirect('/dashboard')
    args={}
    args.update(csrf(request))
    args['form'] = New_Car_Form()
    print(args)
    return render(request, 'rc/new_car.html', args)

@login_required(login_url="/login")
def edit_car(request, unique_id):
    rc_car = RC_Car.objects.get(pk=unique_id)
    if request.method == 'POST':
        form = Edit_Car(request.POST, instance=rc_car)
        if form.is_valid()
            form.save()
            return HttpResponseRedirect('/dashboard/' + unique_id')
    args = {}
    args['form'] = Edit_Car(request.POST, instance=rc_car)
    print(args)
    return render(request, 'rc/'+unique_id+'/edit/', args)
