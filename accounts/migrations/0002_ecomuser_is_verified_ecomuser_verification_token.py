# Generated by Django 5.0.1 on 2024-10-02 10:09

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecomuser',
            name='is_verified',
            field=models.BooleanField(blank=True, default=False, verbose_name='verification'),
        ),
        migrations.AddField(
            model_name='ecomuser',
            name='verification_token',
            field=models.UUIDField(blank=True, default=uuid.uuid4),
        ),
    ]
