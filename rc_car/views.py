from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import New_Car as New_Car_Form, Edit_Car, Change_Password
from .models import RC_Car
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect, Response
from django.forms.models import model_to_dict
from rest_framework import viewsets
from .serializers import Rc_Car_Serializer
from rest_framework.decorators import api_view

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
        return redirect('/dashboard')

    current_user = request.user
    car_owner = rc_car.owner

    if (current_user.id == car_owner.id):
        return render(request, template_name, {'rc' : rc_car, 'car_owner' : True,})

    if (current_user in rc_car.user_list.all()):
        return render(request, template_name, {'rc' : rc_car, 'car_user' : True})

    if (current_user in rc_car.viewer_list.all()):
        return render(request, template_name, {'rc' : rc_car, 'car_viewer' : True})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard'))

@login_required(login_url="/login")
def new_car(request):
    if request.method == 'POST':
        form = New_Car_Form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return HttpResponseRedirect('/dashboard/rc/'+str(obj.id))
    args={}
    args.update(csrf(request))
    args['form'] = New_Car_Form()
    return render(request, 'rc/new_car.html', args)

@login_required(login_url="/login")
def edit_car(request, unique_id):
    try:
        rc_car = RC_Car.objects.get(pk=unique_id)
    except RC_Car.DoesNotExist:
        return redirect('/dashboard')
    if(request.user == rc_car.owner):
        form = Edit_Car(request.POST or None, instance=rc_car)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/rc/' + str(unique_id))
        return render(request, 'rc/edit_car.html', {'form': form,})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard'))

@login_required(login_url="/login")
def change_password(request, unique_id):
    try:
        rc_car = RC_Car.objects.get(pk=unique_id)
    except RC_Car.DoesNotExist:
        return redirect('/dashboard')
    if(request.user == rc_car.owner):
        form = Change_Password(request.POST or None, instance=rc_car)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/rc/' + str(unique_id))
        return render(request, 'rc/edit_car.html', {'form': form,})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard'))

@api_view(['GET'])
def RC_Car_ViewSet_Owned_by(request):
    current_user = request.user
    queryset = RC_Car.objects.filter(owner__id=current_user.id)
    serializer_class = Rc_Car_Serializer(queryset)
    return Response(serializer_class.data)
