# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2021-01-21 06:40
from __future__ import unicode_literals

from django.conf import settings
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
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('auto_id', models.PositiveIntegerField(db_index=True, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_customer_objects', to=settings.AUTH_USER_MODEL)),
                ('updator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='updator_customer_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_added', 'name'),
                'db_table': 'customers_customer',
                'verbose_name': '_(customer)',
                'verbose_name_plural': '_(customers)',
            },
        ),
    ]
