from django.shortcuts import render
from .models import Cart
from products.models import Product
from .forms import CartForm
from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utility import is_user_verified

# Create your views here.

@login_required
@user_passes_test(test_func=is_user_verified, redirect_field_name=None, login_url='/verification-failed/')
def current_products(request):
    if request.method == 'GET':
        items = []
        total_price = 0
        for item in Cart.objects.filter(user=get_user(request)):
            dict_ = {
                'id':item.id,
                'product':item.product,
                'color':item.product_color,
                'size':item.product_size,
                'price':(
                    item.product.original_price + item.product_size.price_to_add + item.product_size.price_to_subtract
                ),
                'product_slug':item.product.slug
            }
            image_item = item.product.product_image.first()
            dict_['image_url'] = image_item.image.url if image_item else None
            items.append(dict_)
            total_price += (
                    item.product.original_price + item.product_size.price_to_add + item.product_size.price_to_subtract
                )
    
        context = {'items':items,'item_count':len(items),'total_price':total_price,'cart':request.GET.get('cart')}
        
        return render(request, 'cart/index.html', context)
    
    if request.method == 'POST':
        color = request.POST.get('color')
        size = request.POST.get('size')
        product_slug = request.GET.get('product_slug')
        form = CartForm({
            'product':product_slug,
            'color':color,
            'size':size
        })
        if form.is_valid():
            data = form.cleaned_data

            try:
                cart_obj = Cart.objects.get(
                    product=data.get('product'),
                    product_color=data.get('color'), 
                    product_size=data.get('size'),
                    user=get_user(request)
                )
                messages.add_message(request, messages.INFO, 'The product is already in your cart.')
            except Cart.DoesNotExist:
                Cart.objects.create(
                    product=data.get('product'),
                    product_color=data.get('color'), 
                    product_size=data.get('size'),
                    user=get_user(request)
                )

    items = []
    total_price = 0
    for item in Cart.objects.filter(user=get_user(request)):
        dict_ = {
            'id':item.id,
            'product':item.product,
            'color':item.product_color,
            'size':item.product_size,
            'price':(
                item.product.original_price + item.product_size.price_to_add + item.product_size.price_to_subtract
            ),
            'product_slug':item.product.slug
        }
        image_item = item.product.product_image.first()
        dict_['image_url'] = image_item.image.url if image_item else None
        items.append(dict_)
        total_price += (
                item.product.original_price + item.product_size.price_to_add + item.product_size.price_to_subtract
            )
    
    context = {'items':items,'item_count':len(items),'total_price':total_price, 'product_slug':product_slug}
    return render(request, 'cart/index.html', context)

@login_required
@user_passes_test(test_func=is_user_verified, redirect_field_name=None, login_url='/verification-failed/')
def remove_item_from_cart(request):
    id = request.GET.get('id')
    product_slug = request.GET.get('product_slug')
    try:
        product = Product.objects.get(slug=product_slug)
        cart_item = Cart.objects.get(id=id,product=product,user=get_user(request))
        cart_item.delete()
        queryset = Cart.objects.filter(user=get_user(request))
    except Exception:
        queryset = Cart.objects.filter(user=get_user(request))
    items = []
    total_price = 0
    for item in queryset:
        items.append({
            'id':item.id,
            'product':item.product,
            'color':item.product_color,
            'size':item.product_size,
            'price':(
                item.product.original_price + item.product_size.price_to_add + item.product_size.price_to_subtract
            ),
            'image_url':item.product.product_image.first().image.url,
            'product_slug':item.product.slug
        })
        total_price += (
                item.product.original_price + item.product_size.price_to_add + item.product_size.price_to_subtract
            )

    context = {'items':items,'item_count':len(items),'total_price':total_price, 'product_slug':product_slug}
    return render(request, 'cart/index.html', context)
