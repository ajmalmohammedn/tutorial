# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2021-01-23 10:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_auto_20210122_1106'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='saleitem',
            options={'ordering': ('-sale',), 'verbose_name': '_(sale item)', 'verbose_name_plural': '_(sale items)'},
        ),
    ]
