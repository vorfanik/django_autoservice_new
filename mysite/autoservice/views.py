from django.shortcuts import render
from django.http import HttpResponse
from .models import AutoModel, Service, Car, Order, OrderingLine

# Create your views here.

def index(request):
    services = Service.objects.count()
    completed_services = Order.objects.filter(status__exact='com').count()
    cars = Car.objects.count()

    # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'services': services,
        'completed_services': completed_services,
        'cars': cars,
    }

    # renderiname base.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)
