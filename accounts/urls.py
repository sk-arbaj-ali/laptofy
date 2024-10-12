from django.urls import path
from .views import create_user_account, login_handler, create_seller_user_account,verify_user, logout_handler, resend_verification_email
from .views import create_new_address

urlpatterns = [
    path('create-user/', create_user_account, name='create-user'),
    path('create-seller-user/', create_seller_user_account, name='create-seller-user'),
    path('login/', login_handler, name='login-page'),
    path('logout-user/', logout_handler, name='logout-page'),
    path('create-new-address/',create_new_address, name='create-new-address'),
    path('verify-user/<token>/', verify_user, name='verify-user'),
    path('resend-verification-email/', resend_verification_email, name='resend-verification-email')
]