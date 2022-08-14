from django.db import models
from datetime import datetime
import pytz
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _

# Create your models here.
utc=pytz.UTC


class AutoModel(models.Model):
    brand = models.CharField(_('Brand'), max_length=200)
    car_model = models.CharField(_('Model'), max_length=200)
    year = models.IntegerField(_('Year'))
    engine = models.CharField(_('Engine'), max_length=200)

    def __str__(self):
        return f"{self.brand} {self.car_model}, {self.engine}, {self.year}"

    class Meta:
        verbose_name = _('Car model')
        verbose_name_plural = _('Car models')


class Service(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    price = models.FloatField(verbose_name=_("Price"), null=True)

    def __str__(self):
        return f"{self.name}: {self.price} euro"

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')


class Car(models.Model):
    client = models.CharField(_('Owner'), max_length=100)
    auto_model_id = models.ForeignKey('AutoModel', verbose_name=_("Car Model"), on_delete=models.SET_NULL, null=True)
    license_plate = models.CharField(_('License plate'), max_length=10)
    vin = models.CharField(_('VIN code'), max_length=20,
                           help_text=_('17 Characters <a href="https://www.vindecoderz.com/">VIN code</a>'))

    image = models.ImageField(_('Image'), upload_to='cars_image', null=True)
    description = HTMLField(_('Description'), null=True)

    def __str__(self):
        return f"{self.client}, {self.auto_model_id}, {self.license_plate}, VIN: {self.vin}"

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class Order(models.Model):
    order_date = models.DateTimeField(_('Order Date'), default=datetime.today().replace(tzinfo=utc))
    return_time = models.DateTimeField(_('Return time'), null=True, blank=True)
    car_id = models.ForeignKey('Car', verbose_name=_("Car"), on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.SET_NULL, null=True, blank=True)

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
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    STATUS = (
        ('con', _('Confirmed')),
        ('pr', _('In progress')),
        ('com', _('Completed')),
        ('can', _('Canceled')),
    )

    status = models.CharField(
        max_length=3,
        choices=STATUS,
        blank=True,
        default='con',
        help_text=_('Status'),
    )


class OrderingLine(models.Model):
    order_id = models.ForeignKey('Order', verbose_name=_("Order"), on_delete=models.SET_NULL, null=True, related_name='order_line')
    service = models.ForeignKey('Service', verbose_name=_("Service"), on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(_("Quantity"))



    @property
    def sum(self):
        return self.service.price * self.quantity

    def __str__(self):
        return f"{self.service} – {self.quantity} pcs "

    class Meta:
        verbose_name = _('Order line')
        verbose_name_plural = _('Order lines')

class OrdersReview(models.Model):
    order = models.ForeignKey('Order', verbose_name=_("Order"), on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    reviewer = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(_('Order Date'), default=datetime.today().replace(tzinfo=utc))
    content = models.TextField(_('Rewiews'), max_length=2000)

    class Meta:
        ordering = ['-date_created']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="default.jpg", upload_to="profile_photo")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (250, 250)
            img.thumbnail(output_size)
            img.save(self.photo.path)