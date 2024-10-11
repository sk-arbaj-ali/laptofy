from django.urls import path
from .views import handle_payment, handle_address, all_orders

urlpatterns = [
    path('checkout-for-payment/<address_id>/', handle_payment, name='checkout-for-payment'),
    path('select-address/', handle_address, name='select-address'),
    path('show-all-orders/', all_orders, name='show-all-orders'),
]