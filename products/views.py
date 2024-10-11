from django.shortcuts import render, redirect
from .forms import ProductForm, CategoryForm, SubCategoryForm, ProductColorAndSizeForm, ProductFilterForm
from .models import Category, SubCategory, Product, ProductColor, ProductSize, ProductImage
from django.http import JsonResponse
from decimal import Decimal
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user
from accounts.utility import login_handler_for_seller, is_user_verified
from django.conf import settings

# Create your views here.

@login_required
@user_passes_test(test_func=is_user_verified, redirect_field_name=None, login_url='/verification-failed/')
@user_passes_test(test_func=login_handler_for_seller, login_url=f"{settings.LOGIN_URL}?seller=0")
def add_product(request):
    if request.method == 'GET':
        productForm = ProductForm()
        productColorAndSizeForm = ProductColorAndSizeForm()
    if request.method == 'POST':
        productForm = ProductForm(request.POST, request.FILES)
        
        if productForm.is_valid():

            # Adding Color and Size. Creating relation with product object
            colors = request.POST.getlist('color')
            sizes = request.POST.getlist('size')
            prices_to_add = request.POST.getlist('price_to_add')
            prices_to_subtract = request.POST.getlist('price_to_subtract')
            available_stocks = request.POST.getlist('available_stock')
            valid_color_and_size_form_list = []
            error_color_and_size_form_list = []
            for index in range(len(colors)):
                productColorAndSizeForm = ProductColorAndSizeForm({
                    'color':colors[index],
                    'size':sizes[index],
                    'price_to_add':prices_to_add[index],
                    'price_to_subtract':prices_to_subtract[index],
                    'available_stock':available_stocks[index]
                })
                if productColorAndSizeForm.is_valid():
                    valid_color_and_size_form_list.append(productColorAndSizeForm)
                else:
                    error_color_and_size_form_list.append(productColorAndSizeForm)

            if not error_color_and_size_form_list:

                data = productForm.cleaned_data

                # Adding Product object
                pobj = Product.objects.create(
                    name=data['name'],
                    brand_name=data['brand_name'],
                    description=data['description'],
                    original_price=data['original_price'],
                    sub_category=data['sub_category'],
                    user=get_user(request)
                )

                for form in valid_color_and_size_form_list:
                    valid_data = form.cleaned_data
                    try:
                        color = pobj.colors.get(name=valid_data['color'])
                    except Exception:
                        color = ProductColor.objects.create(name=valid_data['color'],product=pobj)
                        
                    ProductSize.objects.create(size=valid_data['size'],price_to_add=valid_data['price_to_add'],price_to_subtract=valid_data['price_to_subtract'],available_stock=valid_data['available_stock'],color=color)

                # Adding the Image with Product object
                images = data.get('image')
                for image in images:
                    ProductImage.objects.create(image=image, product=pobj)
            if error_color_and_size_form_list:
                return render(request, 'products/add_product.html', 
                        {
                            'productForm':productForm,
                            'valid_color_and_size_form_list':valid_color_and_size_form_list,
                            'error_color_and_size_form_list':error_color_and_size_form_list
                        }
                )
            else:
                return redirect('/products/add-product/')
    return render(request, 'products/add_product.html', 
                {'productForm':productForm,
                'productColorAndSizeForm':productColorAndSizeForm, 
                }
    )

def add_category(request):
    if request.method == 'GET':
        form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Category.objects.create(name=data['name'])
            return redirect('/products/add-product/')
    return render(request, 'products/add_category.html', {'form':form})

def add_sub_category(request):
    if request.method == 'GET':
        form = SubCategoryForm()
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            SubCategory.objects.create(
                name=data['name'], 
                description=data['description'], 
                category=data['category']
            )
            return redirect('/products/add-product/')
    return render(request, 'products/add_category.html', {'form':form})

def product_detail(request, product_slug=None):
    product = Product.objects.get(slug=product_slug)
    product_images = product.product_image.all()
    product_colors = product.colors.filter(sizes__available_stock__gt=0).distinct()
    first_product_color_sizes = product_colors.first().sizes.filter(available_stock__gt=0).distinct()
    context = {
        'product':product,
        'product_images':product_images,
        'product_colors': product_colors,
        'product_sizes': first_product_color_sizes
    }
    return render(request, 'products/product_detail.html', context)

def product_size_detail(request, product_slug=None, color=None):
    product = Product.objects.get(slug=product_slug)
    product_color = product.colors.get(id=color)
    product_sizes = product_color.sizes.filter(available_stock__gt=0).distinct()
    size_arr = []
    for item in product_sizes:
        size_arr.append({'size':item.size,'id':item.id})
    return JsonResponse(size_arr, safe=False)

def product_size_price_detail(request, product_slug=None, color=None,size=None):
    product = Product.objects.get(slug=product_slug)
    product_color = product.colors.get(id=color)
    product_size = product_color.sizes.get(id=size)
    price = {'price':product.original_price + product_size.price_to_add + product_size.price_to_subtract}
    return JsonResponse(price)


def display_all_products(request):
    if request.method == 'GET':
        product = request.GET.get('product')
        queryset = Product.objects.filter(sub_category__category__name__iexact=product, colors__sizes__available_stock__gt=0).distinct()
        sub_category = SubCategory.objects.filter(category__name__iexact=product)
        sizes = ProductSize.objects.filter(color__product__sub_category__category__name__iexact='laptops').values('size').distinct()
        display_sizes = [('0', '------')]
        for item in sizes:
            display_sizes.append((item['size'], item['size']))
        form = ProductFilterForm(sub_category, display_sizes)
        return render(request, 'products/product-display.html', {'products':queryset, 'form':form})
    
    if request.method == 'POST':
        product = request.GET.get('product')
        queryset = Product.objects.filter(sub_category__category__name__iexact=product, colors__sizes__available_stock__gt=0).distinct()
        sub_category = SubCategory.objects.filter(category__name__iexact=product)
        sizes = ProductSize.objects.filter(color__product__sub_category__category__name__iexact=product).values('size').distinct()
        display_sizes = [('0', '------')]
        for item in sizes:
            display_sizes.append((item['size'], item['size']))
        form = ProductFilterForm(sub_category, display_sizes, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            products = Product.objects.filter(
                sub_category=data.get('product_category'),
                colors__sizes__size=data.get('display_sizes')
            ).distinct()

        return render(request, 'products/product-display.html', {'products':products, 'form':form})
        

def search_products(request):
    if request.method == 'GET':
        return redirect('/home')

    if request.method == 'POST':
        search_data = request.POST.get('search')
        products = Product.objects.filter(name__icontains=search_data)

        category = products[0].sub_category.category
        sub_category = category.subcategory_set.all()
        sizes = ProductSize.objects.filter(color__product__sub_category__category=category).values('size').distinct()
        display_sizes = [('0', '------')]
        for item in sizes:
            display_sizes.append((item['size'], item['size']))
        form = ProductFilterForm(sub_category, display_sizes)

        return render(request, 'products/product-display.html', {'products':products, 'form':form})
    

def filter_products(request):
    if request.method == 'POST':
        sub_category = SubCategory.objects.all()
        sizes = ProductSize.objects.values('size').distinct()
        display_sizes = [('0', '------')]
        for item in sizes:
            display_sizes.append((item['size'], item['size']))
        form = ProductFilterForm(sub_category, display_sizes, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            if data.get('product_category'):
                products = Product.objects.filter(
                    sub_category=data.get('product_category')
                )

            if data.get('display_sizes') != '0':
                products.filter(
                    colors__sizes__size=Decimal(data.get('display_sizes')), 
                    colors__sizes__available_stock__gt=0
                ).distinct()

            if data.get('prices'):
                price = int(data.get('price'))
                if price != 80000:
                    products.filter(original_price__range=(price, price+20000))
                else:
                    products.filter(original_price__gte=80000)

            
        category = products[0].sub_category.category
        sub_category = category.subcategory_set.all()
        sizes = ProductSize.objects.filter(color__product__sub_category__category=category).values('size').distinct()
        display_sizes = [('0', '------')]
        for item in sizes:
            display_sizes.append((item['size'], item['size']))
        form = ProductFilterForm(sub_category, display_sizes)

        return render(request, 'products/product-display.html', {'products':products, 'form':form})