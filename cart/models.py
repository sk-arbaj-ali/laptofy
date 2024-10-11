from django.db import models
from products.models import Product, ProductColor, ProductSize
from django.contrib.auth import get_user_model

# Create your models here.

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    added_at = models.DateField(auto_now_add=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)