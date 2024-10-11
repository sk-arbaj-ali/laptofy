from django.urls import path
from .views import index, show_verification_failed

app_label = 'base'

urlpatterns = [
    path('', index, name='home'),
    path('verification-failed/', show_verification_failed, name='verification-failed'),
]