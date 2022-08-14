from .models import Service, Car, Order, OrderingLine
from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import OrderReviewForm, ProfileUpdateForm, UserUpdateForm, UserOrderCreateForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _


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


class OrdersListView(ListView):
    model = Order
    paginate_by = 2
    template_name = 'orders_list.html'
    context_object_name = 'orders'


class OrdersDetailView(FormMixin, DetailView):
    model = Order
    template_name = 'orders_detail.html'
    context_object_name = 'orders'
    form_class = OrderReviewForm

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse('order_datails', kwargs={'pk': self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(OrdersDetailView, self).form_valid(form)


def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Car.objects.filter(
        Q(client__icontains=query) | Q(vin__icontains=query) | Q(license_plate__icontains=query) | Q(
            auto_model_id__brand__icontains=query) | Q(auto_model_id__car_model__icontains=query))
    return render(request, 'search.html', {'cars': search_results, 'query': query})


# cRud
class OrdersByUserListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'user_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).filter(status__exact='con').order_by('return_time')


# cRud
class UserOrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'user_order_detail.html'
    context_object_name = 'orders'


# Crud
class OrderByUserCreateView(LoginRequiredMixin, CreateView):
    model = Order
    # fields = ['car_id', 'return_time', 'status']
    success_url = "/service/myorders/"
    template_name = 'user_order_form.html'
    form_class = UserOrderCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Crud
class OrderLineByUserCreateView(LoginRequiredMixin, CreateView):
    model = OrderingLine
    fields = ['service', 'quantity']
    template_name = 'user_order_line_form.html'

    def get_success_url(self):
        return reverse('my_order', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.order_id = Order.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)


# crUd
class OrderLineByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = OrderingLine
    fields = ['service', 'quantity']
    template_name = 'user_order_line_form.html'

    def get_success_url(self):
        return reverse('my_order', kwargs={'pk': self.object.order_id.id})

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.order_id.user


# cruD
class OrderLineByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OrderingLine
    template_name = 'order_line_delete.html'

    def get_success_url(self):
        return reverse('my_order', kwargs={'pk': self.object.order_id.id})

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.order_id.user


# crUd
class OrderByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    fields = ['car_id', 'return_time', 'status']
    success_url = "/service/myorders/"
    template_name = 'user_order_form.html'
    # form_class = UserOrderCreateForm


    def test_func(self):
        order = self.get_object()
        return self.request.user == order.user


# cruD
class OrderByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    success_url = "/service/myorders/"
    template_name = 'user_order_delete.html'

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.user


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, _('User name %s already exists!') % username)
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, _('User with email Email %s is already registered!') % email)
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    return redirect('login')
        else:
            messages.error(request, _('Passwords do not match!'))
            return redirect('register')
    return render(request, 'registration/register.html')


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def profile_update(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, _("Profile updated"))
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile_update.html', context)
