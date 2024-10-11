from django.db import models
from django.template.defaultfilters import slugify
import uuid
from django.contrib.auth import get_user_model

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'

class Product(models.Model):
    name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100, null=True)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True,null=True, blank=True)
    original_price = models.IntegerField(default=0)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name + ' ' + self.description[:10] + str(uuid.uuid4()))
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')

class ProductColor(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')

    def __str__(self):
        return f'{self.name}'
    
class ProductSize(models.Model):
    size = models.DecimalField(max_digits=4, decimal_places=2, help_text='Provide the size in scale of inch')
    price_to_add = models.IntegerField(default=0)
    price_to_subtract = models.IntegerField(default=0)
    available_stock = models.IntegerField(default=0)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, related_name='sizes')

    def __str__(self):
        return f'{self.size}'

# class ProductColor(models.Model):
#     name = models.CharField(max_length=50)
#     sizes = models.ManyToManyField('ProductSize', through='Inter_Color_Size')

#     def __str__(self):
#         return f'{self.name}'
    
# class ProductSize(models.Model):
#     size = models.DecimalField(max_digits=4, decimal_places=2, help_text='Provide the size in scale of inch')

#     def __str__(self):
#         return f'{self.size}'

# class Inter_Color_Size(models.Model):
#     color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
#     size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
#     price_to_add = models.IntegerField(default=0)
#     price_to_subtract = models.IntegerField(default=0)
#     available_stock = models.IntegerField(default=0)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='color_and_size')