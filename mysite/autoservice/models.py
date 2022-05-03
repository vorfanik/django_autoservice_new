from django.db import models


# Create your models here.

class AutoModel(models.Model):
    brand = models.CharField('Brand', max_length=200)
    car_model = models.CharField('Model', max_length=200)
    year = models.IntegerField('Year')
    engine = models.CharField('Engine', max_length=200)

    def __str__(self):
        return f"{self.brand}, {self.car_model}, {self.engine}, {self.year}"

    class Meta:
        verbose_name = 'Car model'
        verbose_name_plural = 'Car models'


class Service(models.Model):
    name = models.CharField('Name', max_length=200)
    price = models.FloatField(verbose_name="Price")

    def __str__(self):
        return f"{self.name}: {self.price}"

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class Car(models.Model):
    client = models.CharField('Owner', max_length=100)
    auto_model_id = models.ForeignKey('AutoModel', verbose_name="Car Model", on_delete=models.SET_NULL, null=True)
    license_plate = models.CharField('License plate', max_length=10)
    vin = models.CharField('VIN code', max_length=20,
                           help_text='17 Characters <a href="https://www.vindecoderz.com/">VIN code</a>')

    def __str__(self):
        return f"{self.client}: {self.auto_model_id}, {self.license_plate}, VIN: {self.vin}"

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'


class Order(models.Model):
    order_date = models.DateTimeField('Order Date', auto_now_add=True)
    car_id = models.ForeignKey('Car', verbose_name="Car", on_delete=models.SET_NULL, null=True)

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
        ('p', 'Confirmed'),
        ('v', 'In progress'),
        ('a', 'Completed'),
        ('t', 'Canceled'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='p',
        help_text='Status',
    )


class OrderingLine(models.Model):
    order_id = models.ForeignKey('Order', verbose_name="Order", on_delete=models.SET_NULL, null=True)
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
