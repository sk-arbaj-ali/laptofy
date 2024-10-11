from django.db import models
import uuid
from products.models import Product, ProductColor, ProductSize
from django.contrib.auth import get_user_model

# Create your models here.

class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, blank=True, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    final_price = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)