from django.shortcuts import render

from .models import RC_Car

# Create your views here.

def index(request):
    template_name = 'dashboard/index.html'
    return render(request, template_name)

def by_uuid(request, unique_id):
    return 0
