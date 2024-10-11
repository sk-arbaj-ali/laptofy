from django.urls import path
from .views import add_category, add_sub_category, add_product, product_detail, product_size_detail,product_size_price_detail,display_all_products, search_products, filter_products

urlpatterns = [
    path('add-product/', add_product, name='add-product'),
    path('add-category/', add_category, name='add-category'),
    path('add-sub-category/', add_sub_category, name='add-sub-category'),
    path('product-detail/<slug:product_slug>/', product_detail, name='product-detail'),
    path('fetch-size-detail/<slug:product_slug>/<color>/', product_size_detail, name='product-size-detail'),
    path('fetch-size-price-detail/<slug:product_slug>/<color>/<size>/', product_size_price_detail, name='product-size-price-detail'),
    path('display-products/', display_all_products, name='display-products'),
    path('search-products/', search_products, name='search-products'),
    path('apply-filters/', filter_products, name='apply-filters'),
]