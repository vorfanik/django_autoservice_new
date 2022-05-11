from django.db import models
from datetime import datetime
import pytz
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.
utc=pytz.UTC


class AutoModel(models.Model):
    brand = models.CharField('Brand', max_length=200)
    car_model = models.CharField('Model', max_length=200)
    year = models.IntegerField('Year')
    engine = models.CharField('Engine', max_length=200)

    def __str__(self):
        return f"{self.brand} {self.car_model}, {self.engine}, {self.year}"

    class Meta:
        verbose_name = 'Car model'
        verbose_name_plural = 'Car models'


class Service(models.Model):
    name = models.CharField('Name', max_length=200)
    price = models.FloatField(verbose_name="Price", null=True)

    def __str__(self):
        return f"{self.name}: {self.price} euro"

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class Car(models.Model):
    client = models.CharField('Owner', max_length=100)
    auto_model_id = models.ForeignKey('AutoModel', verbose_name="Car Model", on_delete=models.SET_NULL, null=True)
    license_plate = models.CharField('License plate', max_length=10)
    vin = models.CharField('VIN code', max_length=20,
                           help_text='17 Characters <a href="https://www.vindecoderz.com/">VIN code</a>')

    image = models.ImageField('Image', upload_to='cars_image', null=True)
    description = HTMLField('Description', null=True)

    def __str__(self):
        return f"{self.client}, {self.auto_model_id}, {self.license_plate}, VIN: {self.vin}"

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'


class Order(models.Model):
    order_date = models.DateTimeField('Order Date', default=datetime.today().replace(tzinfo=utc))
    return_time = models.DateTimeField('Return time', null=True, blank=True)
    car_id = models.ForeignKey('Car', verbose_name="Car", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.return_time and datetime.today().replace(tzinfo=utc) > self.return_time:
            return True
        return False

    @property
    def sum(self):
        order_line = OrderingLine.objects.filter(order_id=self.id)
        sum = 0
        for line in order_line:
            sum += line.quantity * line.service.price
        return sum

    def __str__(self):
        return f"{self.car_id}, {self.order_date}. Total Sum: {self.sum}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    STATUS = (
        ('con', 'Confirmed'),
        ('pr', 'In progress'),
        ('com', 'Completed'),
        ('can', 'Canceled'),
    )

    status = models.CharField(
        max_length=3,
        choices=STATUS,
        blank=True,
        default='p',
        help_text='Status',
    )


class OrderingLine(models.Model):
    order_id = models.ForeignKey('Order', verbose_name="Order", on_delete=models.SET_NULL, null=True, related_name='order_line')
    service = models.ForeignKey('Service', verbose_name="Service", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField("Quantity")



    @property
    def sum(self):
        return self.service.price * self.quantity

    def __str__(self):
        return f"{self.service} – {self.quantity}: , "

    class Meta:
        verbose_name = 'Order line'
        verbose_name_plural = 'Order lines'

class OrdersReview(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField('Order Date', default=datetime.today().replace(tzinfo=utc))
    content = models.TextField('Rewiew', max_length=2000)
