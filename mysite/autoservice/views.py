from django.shortcuts import render
from django.http import HttpResponse
from .models import AutoModel, Service, Car, Order, OrderingLine
from django.shortcuts import render, get_object_or_404
from django.views import generic

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

def cars(request):
    cars = Car.objects.all()
    context = {
        'cars': cars
    }
    return render(request, 'cars.html', context=context)

def car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car.html', {'car': car})


class OrdersListView(generic.ListView):
    model = Order
    template_name = 'orders_list.html'
    context_object_name = 'orders'

class OrdersDetailView(generic.DetailView):
    model = Order
    template_name = 'orders_detail.html'
    context_object_name = 'orders'