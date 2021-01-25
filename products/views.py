from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from main.functions import get_auto_id, get_a_id, generate_form_errors
from django.db.models import Q
import json
import datetime
from products.models import Product
from products.forms import ProductForm
from dal import autocomplete


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Product.objects.none()

        items = Product.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(name__icontains=query))

        return items

def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updator = request.user
            data.auto_id = get_auto_id(Product)
            data.save()

            response_data = {
                'status': 'true',
                'title': 'Successfully Created',
                'message': 'Product Successfully Created',
                'redirect': 'true',
                'redirect_url': reverse('products:product', kwargs={"pk": data.pk})
            }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                'Status': 'false',
                'stable': 'true',
                'title': 'Form Validation Error',
                'message': message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = ProductForm()
        context = {
            'form': form,
            'title': 'Create Product',
            'redirect': True,
            'url': reverse('products:create'),

            "is_need_select_picker" : True,
            "is_need_popup_box" : True,
            "is_need_custom_scroll_bar" : True,
            "is_need_wave_effect" : True,
            "is_need_bootstrap_growl" : True,
            "is_need_chosen_select" : True,
            "is_need_grid_system" : True,
            "is_need_datetime_picker" : True,
            "is_need_animations": True,
            "is_dashboard" :True
        }
        return render(request, 'products/entry.html', context)
        

def edit(request, pk):
    instance = get_object_or_404(Product.objects.filter(pk=pk))
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()

            response_data = {
                'status': 'true',
                'title': 'Successfully Updated',
                'message': 'Product Successfully Updated',
                'redirect': 'true',
                'redirect_url': reverse('products:product', kwargs={"pk": data.pk})
            }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                'Status': 'false',
                'stable': 'true',
                'title': 'Form Validation Error',
                'message': message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = ProductForm(instance=instance)
        context = {
            'form': form,
            'title': 'Edit Product',
            'redirect': True,
            'url': reverse('products:edit', kwargs={'pk':instance.pk}),

            "is_need_select_picker" : True,
            "is_need_popup_box" : True,
            "is_need_custom_scroll_bar" : True,
            "is_need_wave_effect" : True,
            "is_need_bootstrap_growl" : True,
            "is_need_chosen_select" : True,
            "is_need_grid_system" : True,
            "is_need_datetime_picker" : True,
            "is_need_animations": True,
            "is_dashboard" :True
        }
        return render(request, 'products/entry.html', context)


def products(request):
    instances = Product.objects.filter(is_deleted=False)
    context = {
        'title': 'Products',
        'instances': instances,

        "is_need_select_picker" : True,
        "is_need_popup_box" : True,
        "is_need_custom_scroll_bar" : True,
        "is_need_wave_effect" : True,
        "is_need_bootstrap_growl" : True,
        "is_need_chosen_select" : True,
        "is_need_grid_system" : True,
        "is_need_datetime_picker" : True,
        "is_need_animations": True,
        "is_dashboard" :True
    }
    return render(request, 'products/products.html', context)


def product(request, pk):
    instance = get_object_or_404(Product.objects.filter(pk=pk))
    context = {
        'title': 'Product' + instance.name,
        'instance': instance,

        "is_need_select_picker" : True,
        "is_need_popup_box" : True,
        "is_need_custom_scroll_bar" : True,
        "is_need_wave_effect" : True,
        "is_need_bootstrap_growl" : True,
        "is_need_chosen_select" : True,
        "is_need_grid_system" : True,
        "is_need_datetime_picker" : True,
        "is_need_animations": True,
        "is_dashboard" :True
    }
    return render(request, 'products/product.html', context)


def delete(request, pk):
    Product.objects.filter(pk=pk).update(is_deleted=True)
    response_data = {
        "status" : "true",
        "title" : "Successfully Deleted",
        "message" : "Product Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('customers:customers')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')