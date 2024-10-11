from django.shortcuts import render, redirect
from .forms import AddressForm
from .models import Address
from .forms import UserCreationForm, CustomAuthForm
from django.contrib.auth import login, get_user, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from .utility import is_user_verified, send_verification_email
from django.conf import settings

# # Create your views here.

def create_user_account(request):
    if request.method == 'GET':
        form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.add_message(request, messages.SUCCESS, 'Account created successfully. Please go to login.')
            messages.add_message(request, messages.SUCCESS, 'Check your email for verification.')

            verification_url = settings.ALLOWED_HOSTS[0] + reverse('verify-user', kwargs={'token':str(user.verification_token)})
            message = f'To verify your account, please click the link : {verification_url}'
            send_verification_email(message, user.email)

            return render(request, 'accounts/create-user.html', {'form':form})

    return render(request, 'accounts/create-user.html', {'form':form})

def create_seller_user_account(request):
    if request.method == 'GET':
        form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_seller = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Seller Account created. Please go to login.')
            messages.add_message(request, messages.SUCCESS, 'Check your email for verification.')
            return render(request, 'accounts/create-user.html', {'form':form})

    return render(request, 'accounts/create-user.html', {'form':form})


def login_handler(request):
    if request.method == 'GET':
        form = CustomAuthForm(request)
        seller = request.GET.get('seller')
    if request.method == 'POST':
        form = CustomAuthForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user=user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('/')
        return render(request, 'accounts/login-user.html', {'form':form})
    return render(request, 'accounts/login-user.html', {'form':form, 'seller':seller})


def logout_handler(request):
    logout(request)
    return redirect(reverse('home'))
    

@login_required
@user_passes_test(test_func=is_user_verified, redirect_field_name=None, login_url='/verification-failed/')
def create_new_address(request):
    if request.method == 'GET':
        form = AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Address.objects.create(
                city=data['city'],
                street=data['street'],
                landmark=data['landmark'],
                pincode=data['pincode'],
                phone=data['phone'],
                user=get_user(request)
            )
            return redirect('/orders/select-address/')
    return render(request, 'accounts/add-new-address.html',{'form':form})
    

@login_required
def verify_user(request, token=None):
    if token == None:
        return redirect(reverse('home'))
    user = get_user(request)
    user_token = str(user.verification_token)
    if user_token == token:
        user.is_verified = True
        user.save()
        return redirect(reverse('home'))