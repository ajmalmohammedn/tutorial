from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from main.models import BaseModel


class Customer(BaseModel):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.TextField()

    class Meta:
        db_table = 'customers_customer'
        verbose_name = '_(customer)'
        verbose_name_plural = '_(customers)'
        ordering = ('-date_added', 'name')

    def __unicode__(self):
        return str(self.name)