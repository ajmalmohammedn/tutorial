from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import TextInput, Textarea, Select
from products.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['auto_id', 'creator', 'updator', 'is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Name'}),
            'price': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Price'}),
            'cost': TextInput(attrs={'class': 'form-control', 'placeholder': 'Cost'}),
            'stock': Textarea(attrs={'class': 'form-control', 'placeholder': 'Stock'})

        }
        error_messages = {
            'name' : {
                'required' : _("Name field is required."),
            },
            'price' : {
                'required' : _("Price field is required."),
            },
            'cost' : {
                'required' : _("Cost field is required."),
            },
            'stock' : {
                'required' : _("Stock field is required."),
            }
        }


        