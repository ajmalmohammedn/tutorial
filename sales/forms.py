from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import TextInput, Textarea, Select
from sales.models import Sale, SaleItem
from dal import autocomplete


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ['auto_id', 'creator', 'updator', 'is_deleted', 'subtotal', 'total']
        widgets = {
            'customer': autocomplete.ModelSelect2(url='customers:customer_autocomplete',attrs={'data-placeholder': 'Customer','data-minimum-input-length': 1},),
            'date': TextInput(attrs={'class': 'required date-picker form-control', 'placeholder': 'Date'}),
            'discount': TextInput(attrs={'class': 'form-control', 'placeholder': 'Discount'}),
        }
        error_messages = {
            'customer' : {
                'required' : _("Customer field is required."),
            },
            'date' : {
                'required' : _("Date field is required."),
            },
            'discount' : {
                'required' : _("Discount field is required."),
            }
        }


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        exclude = ['sale']
        widgets = {
            'product': autocomplete.ModelSelect2(url='products:product_autocomplete',attrs={'data-placeholder': 'Product','data-minimum-input-length': 1},),
            'qty': TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),

        }
        error_messages = {
            'product' : {
                'required' : _("Product field is required."),
            },
            'qty' : {
                'required' : _("Quantity field is required."),
            }
        }