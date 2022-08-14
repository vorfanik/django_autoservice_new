from django.contrib import admin
from .models import AutoModel, Service, Car, Order, OrderingLine, OrdersReview, Profile

# Register your models here.

class ServiceInstanceInline(admin.TabularInline):
    model = OrderingLine
    can_delete = False
    extra = 0 # išjungia placeholder'ius

class CarAdmin(admin.ModelAdmin):
    list_display = ('client', 'auto_model_id', 'license_plate', 'vin')
    list_filter = ('client', 'auto_model_id')
    search_fields = ('license_plate', 'vin')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('car_id', 'user', 'order_date', 'return_time', 'sum', 'status')
    list_editable = ('status', 'return_time',)
    fieldsets = (
        ('General', {'fields': ('car_id', 'user')}),
        ('Availability', {'fields': ('status', 'return_time')}),
    )
    inlines = [ServiceInstanceInline]

class OrderLinesAdmin(admin.ModelAdmin):
    list_display = ('service', 'quantity')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class OrdersReviewAdmin(admin.ModelAdmin):
    list_display = ('order', 'date_created', 'reviewer', 'content')

admin.site.register(OrdersReview, OrdersReviewAdmin)
admin.site.register(AutoModel)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderingLine, OrderLinesAdmin)
admin.site.register(Profile)