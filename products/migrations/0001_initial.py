# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2021-01-22 05:24
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('auto_id', models.PositiveIntegerField(db_index=True, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=128)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('stock', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_product_objects', to=settings.AUTH_USER_MODEL)),
                ('updator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='updator_product_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_added', 'name'),
                'db_table': 'products_product',
                'verbose_name': '_(product)',
                'verbose_name_plural': '_(products)',
            },
        ),
    ]
