from django.urls import path
from .views import current_products, remove_item_from_cart

urlpatterns = [
    path('current-added-products/', current_products, name='current-added-products'),
    path('remove-item-from-cart/', remove_item_from_cart, name='remove-item-from-cart'),
]