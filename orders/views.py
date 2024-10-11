from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import  SelectAddressForm
from .models import ProductOrder, Order
from cart.models import Cart
from accounts.models import Address
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utility import is_user_verified

# Create your views here.

@login_required
@user_passes_test(test_func=is_user_verified, redirect_field_name=None, login_url='/verification-failed/')
def handle_payment(request, address_id=None):
    if not address_id:
        return redirect(reverse('select-address'))
    if request.method == 'POST':
        payment = request.POST.get('payment')
        if payment and payment.lower() == 'cod':

            cart_queryset = Cart.objects.filter(user=get_user(request))
            Order_ID = Order.objects.create(user=get_user(request))
            for item in cart_queryset:
                pobj = ProductOrder(
                    product=item.product,
                    product_color=item.product_color,
                    product_size=item.product_size,
                    final_price=(item.product.original_price + item.product_size.price_to_add + item.product_size.price_to_subtract),
                    order=Order_ID
                )
                pobj.save()
            cart_queryset.delete()
            
            return redirect(reverse('show-all-orders'))
        
    return render(request, 'orders/select-payment.html', {'address_id':address_id})


@login_required
@user_passes_test(test_func=is_user_verified, redirect_field_name=None, login_url='/verification-failed/')
def handle_address(request):
    if request.method == 'GET':
        # if there is no product in cart then it doesn't make sence
        # to select address so redirect to cart with a message
        if not Cart.objects.filter(user=get_user(request)):
            return redirect(f"{reverse('current-added-products')}?cart=false")
        
        queryset = Address.objects.filter(user=get_user(request))
    if request.method == 'POST':
       form = SelectAddressForm(request.POST)
       if form.is_valid():
            address = form.cleaned_data.get('address')
            return redirect(reverse('checkout-for-payment', kwargs={'address_id':address.id}))
       
    return render(request, 'orders/select-address.html', {'addresses':queryset})

@login_required
@user_passes_test(test_func=is_user_verified, redirect_field_name=None, login_url='/verification-failed/')
def all_orders(request):
    orders = Order.objects.filter(user=get_user(request))
    product_orders = []
    for order in orders:
        for item in order.productorder_set.all():
            product_orders.append(item)
    return render(request, 'orders/all-orders.html', {'orders':product_orders})