from django.contrib import admin
from .models import AutoModel, Service, Car, Order, OrderingLine

# Register your models here.

class ServiceInstanceInline(admin.TabularInline):
    model = OrderingLine
    can_delete = False
    extra = 0 # išjungia placeholder'ius

class OrderAdmin(admin.ModelAdmin):
    list_display = ('car_id', 'order_date')
    inlines = [ServiceInstanceInline]

class CarAdmin(admin.ModelAdmin):
    list_display = ('client', 'auto_model_id', 'license_plate', 'vin')

admin.site.register(AutoModel)
admin.site.register(Service)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderingLine)