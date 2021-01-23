from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from main.models import BaseModel


class Sale(BaseModel):
    customer = models.ForeignKey('customers.Customer', limit_choices_to={'is_deleted': False})
    date = models.DateField()
    subtotal = models.DecimalField(default=0.00, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    discount = models.DecimalField(default=0.00, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'sales_sale'
        verbose_name = '_(sale)'
        verbose_name_plural = '_(sale)'
        ordering = ('-date',)

    def __unicode__(self):
        return str(self.auto_id)


class SaleItem(models.Model):
    sale = models.ForeignKey('sales.Sale')
    product = models.ForeignKey('products.Product', limit_choices_to={'is_deleted': False})
    qty = models.DecimalField(default=0.00, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))]) 

    class Meta:
        db_table = 'sales_sale item'
        verbose_name = '_(sale item)'
        verbose_name_plural = '_(sale items)'
        ordering = ('sale',)

    def subtotal(self):
        return self.qty * self.product.price

    def __unicode__(self):
        return str(self.sale.auto_id)