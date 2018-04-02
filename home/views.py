from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .forms import MyRegistrationForm
from django.urls import reverse
from django.template.context_processors import csrf

# Create your views here.


def index(request):
    template_name = 'home/index.html'
    return render(request, template_name)


def register(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)     # create form object
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    args = {}
    args.update(csrf(request))
    args['form'] = MyRegistrationForm()
    print(args)
    return render(request, 'home/register.html', args)
