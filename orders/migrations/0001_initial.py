# Generated by Django 5.0.1 on 2024-09-23 14:20

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.UUIDField(blank=True, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_price', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('product_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productcolor')),
                ('product_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productsize')),
            ],
        ),
    ]
