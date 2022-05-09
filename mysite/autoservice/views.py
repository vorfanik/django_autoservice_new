from django.shortcuts import render
from django.http import HttpResponse
from .models import AutoModel, Service, Car, Order, OrderingLine
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def index(request):
    services = Service.objects.count()
    completed_services = Order.objects.filter(status__exact='com').count()
    cars = Car.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'services': services,
        'completed_services': completed_services,
        'cars': cars,
        'num_visits': num_visits,
    }

    # renderiname base.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)

def cars(request):
    paginator = Paginator(Car.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_car = paginator.get_page(page_number)
    context = {
        'cars': paged_car
    }
    return render(request, 'cars.html', context=context)

def car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car.html', {'car': car})


class OrdersListView(generic.ListView):
    model = Order
    paginate_by = 2
    template_name = 'orders_list.html'
    context_object_name = 'orders'

class OrdersDetailView(generic.DetailView):
    model = Order
    template_name = 'orders_detail.html'
    context_object_name = 'orders'

def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Car.objects.filter(Q(client__icontains=query) | Q(vin__icontains=query) | Q(license_plate__icontains=query) | Q(auto_model_id__brand__icontains=query) | Q(auto_model_id__car_model__icontains=query))
    return render(request, 'search.html', {'cars': search_results, 'query': query})