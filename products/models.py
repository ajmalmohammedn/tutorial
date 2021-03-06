from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from main.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=128)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    cost = models.DecimalField(default=0.00, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    stock = models.DecimalField(default=0.00, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'products_product'
        verbose_name = '_(product)'
        verbose_name_plural = '_(products)'
        ordering = ('-date_added', 'name')

    def __unicode__(self):
        return str(self.name)