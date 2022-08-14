from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_id>', views.car, name='car'),
    path('orders/', views.OrdersListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrdersDetailView.as_view(), name='order_datails'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('myorders/', views.OrdersByUserListView.as_view(), name='my_orders'),
    path('myorders/<int:pk>', views.UserOrderDetailView.as_view(), name='my_order'),
    path('myorders/new', views.OrderByUserCreateView.as_view(), name='my_order_new'),
    path('myorders/<int:pk>/update', views.OrderByUserUpdateView.as_view(), name='my_order_update'),
    path('myorders/<int:pk>/delete', views.OrderByUserDeleteView.as_view(), name='my_order_delete'),
    path('myorders/<int:pk>/orderline/new', views.OrderLineByUserCreateView.as_view(), name='my_order_line_create'),
    path('myorders/orderline/<int:pk>/update', views.OrderLineByUserUpdateView.as_view(), name='my_order_line_update'),
    path('myorders/<int:pk>/orderline/delete', views.OrderLineByUserDeleteView.as_view(), name='my_order_line_delete'),

]