from django.shortcuts import render, redirect
from products.models import Product
# from django.db.models import F
from django.contrib.auth.decorators import user_passes_test, login_required
from accounts.utility import is_user_verified

# Create your views here.


def index(request):
    laptops = Product.objects.filter(colors__sizes__available_stock__gt=0)\
            .filter(sub_category__category__name__iexact='laptops')\
            .order_by('created_at').distinct()[:6]
    desktops = Product.objects.filter(colors__sizes__available_stock__gt=0)\
            .filter(sub_category__category__name__iexact='desktops')\
            .order_by('created_at').distinct()[:6]
    monitors = Product.objects.filter(colors__sizes__available_stock__gt=0)\
            .filter(sub_category__category__name__iexact='monitors')\
            .order_by('created_at').distinct()[:6]

    context = {
        'laptops':laptops,
        'desktops':desktops,
        'monitors':monitors
    }
    return render(request, 'base/index.html', context)


@login_required
def show_verification_failed(request):
    if request.user.is_verified:
        return redirect('/')
    return render(request, 'base/verification.html')