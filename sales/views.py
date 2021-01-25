from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from main.functions import get_auto_id, get_a_id, generate_form_errors
from django.forms import formset_factory, inlineformset_factory
from django.forms.widgets import TextInput, Textarea, Select
from django.db.models import Q
import json
import datetime
from sales.forms import SaleForm, SaleItemForm
from sales.models import Sale, SaleItem
from products.functions import update_stock
from products.models import Product
from products.views import autocomplete

def create(request):
    SaleItemFormset = formset_factory(SaleItemForm, extra=1)
    if request.method == 'POST':
        form = SaleForm(request.POST)
        sale_item_formset = SaleItemFormset(request.POST, prefix='sale_item_formset')
        if form.is_valid() and sale_item_formset.is_valid():

            # Creating Sale Item Objects for finding duplicate product entry
            items = {}
            for f in sale_item_formset:  
                product = f.cleaned_data['product']
                qty = f.cleaned_data['qty']
                if str(product.pk) in items:
                    q = items[str(product.pk)]["qty"]
                    items[str(product.pk)]["qty"] = q + qty
                else:
                    dic = {
                        "qty" : qty,
                    }
                    items[str(product.pk)] = dic 

            # Checking the stock available for this product
            stock_ok = True
            error_message = ''
            for key, value in items.items():
                product = Product.objects.get(pk=key)
                stock = product.stock
                qty = value['qty']
                if qty > stock:
                    stock_ok = False
                    error_message += "{} has only {} in stock, You entered {} qty".format(product.name,str(stock),str(qty))

            if stock_ok:
                discount = form.cleaned_data['discount']
                data = form.save(commit=False)
                data.creator = request.user
                data.updator = request.user
                data.auto_id = get_auto_id(Sale)
                data.save()

                subtotal = 0
                for key, value in items.items():
                    product = Product.objects.get(pk=key)
                    qty = value["qty"]
                    price = product.price
                    sub = (qty * price)
                    subtotal += sub 
                    
                    SaleItem(
                        sale = data,
                        product = product,
                        qty = qty
                    ).save()

                    update_stock(product.pk, qty, 'decrease')

                total = subtotal - discount
                data.subtotal = subtotal
                data.total = total
                data.save()
                    
                response_data = {
                    "status" : "true",
                    "title" : "Successfully Created",
                    "message" : "Sale Successfully Created.",
                    "redirect" : "true",
                    "redirect_url" : reverse('sales:sale',kwargs={'pk':data.pk})
                }
            else:
                response_data = {
                    "status" : "false",
                    "stable" : "true",
                    "title" : "Out of Stock",
                    "message" : error_message
                }
        else:
            message = generate_form_errors(form,formset=False)     
            message += generate_form_errors(sale_item_formset,formset=True)
            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }  
            
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = SaleForm()
        sale_item_formset = SaleItemFormset(prefix='sale_item_formset')
        context = {
            'title': 'Create Sale',
            'form': form,
            'sale_item_formset': sale_item_formset,
            'redirect': True,
            'url': reverse('sales:create'),

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
        return render(request, 'sales/entry.html', context)


def edit(request, pk):
    instance = get_object_or_404(Sale.objects.filter(pk=pk))
    if SaleItem.objects.filter(sale=instance).exists():
        extra = 0
    else:
        extra = 1

    SaleItemFormset = inlineformset_factory(
            Sale,
            SaleItem,
            can_delete = True,
            extra = extra,
            exclude = ('sale',),
            widgets = {
            'product': autocomplete.ModelSelect2(url='products:product_autocomplete',attrs={'data-placeholder': 'Product','data-minimum-input-length': 1},),
            'qty': TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            }
        )

    if request.method == 'POST':
        form = SaleForm(request.POST, instance=instance)
        sale_item_formset = SaleItemFormset(request.POST, prefix='sale_item_formset', instance=instance)
        if form.is_valid() and sale_item_formset.is_valid():

            # Creating Sale Item Objects for finding duplicate product entry
            items = {}
            for f in sale_item_formset:  
                product = f.cleaned_data['product']
                qty = f.cleaned_data['qty']
                if str(product.pk) in items:
                    q = items[str(product.pk)]["qty"]
                    items[str(product.pk)]["qty"] = q + qty
                else:
                    dic = {
                        "qty" : qty,
                    }
                    items[str(product.pk)] = dic 

            # Checking the stock available for this product
            stock_ok = True
            error_message = ''
            for key, value in items.items():
                product = Product.objects.get(pk=key)
                prev_qty = 0
                if SaleItem.objects.filter(sale=instance, product=product).exists():
                    prev_qty = SaleItem.objects.get(sale=instance, product=product).qty   
                stock = product.stock + prev_qty
                qty = value['qty']
                if qty > stock:
                    stock_ok = False
                    error_message += "{} has only {} in stock, You entered {} qty".format(product.name,str(stock),str(qty))

            if stock_ok:
                discount = form.cleaned_data['discount']
                data = form.save(commit=False)
                data.updator = request.user
                data.date_updated = datetime.datetime.now()
                data.save()

                #delete previous items and update stock
                previous_sale_items = SaleItem.objects.filter(sale=instance)
                for p in previous_sale_items:
                    prev_qty = p.qty
                    update_stock(p.product.pk, prev_qty, 'increase')
                previous_sale_items.delete()

                #save items
                subtotal = 0
                for key, value in items.items():
                    product = Product.objects.get(pk=key)
                    qty = value["qty"]
                    price = product.price
                    sub = (qty * price)
                    subtotal += sub 
                    
                    SaleItem(
                        sale = data,
                        product = product,
                        qty = qty
                    ).save()

                    update_stock(product.pk, qty, 'decrease')

                total = subtotal - discount
                data.subtotal = subtotal
                data.total = total
                data.save()
                    
                response_data = {
                    "status" : "true",
                    "title" : "Successfully Updated",
                    "message" : "Sale Successfully Updated.",
                    "redirect" : "true",
                    "redirect_url" : reverse('sales:sale',kwargs={'pk':data.pk})
                }
            else:
                response_data = {
                    "status" : "false",
                    "stable" : "true",
                    "title" : "Out of Stock",
                    "message" : error_message
                }
        else:
            message = generate_form_errors(form,formset=False)     
            message += generate_form_errors(sale_item_formset,formset=True)
            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }  
            
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')


    else:
        form = SaleForm(instance=instance)
        sale_item_formset = SaleItemFormset(prefix='sale_item_formset', instance=instance)
        context = {
            'title': 'Edit Sale',
            'form': form,
            'sale_item_formset': sale_item_formset,
            'redirect': True,
            'url': reverse('sales:edit', kwargs={'pk':instance.pk}),

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
        return render(request, 'sales/entry.html', context)


def sales(request):
    instances = Sale.objects.filter(is_deleted=False)
    query = request.GET.get('q')

    if query:
        instances = instances.filter(Q(customer__name__icontains=query) | Q(customer__email__icontains=query) | Q(customer__phone__icontains=query) | Q(customer__address__icontains=query))

    context = {
        'title': 'Sales',
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
    return render(request, 'sales/sales.html', context)


def sale(request, pk):
    instance = get_object_or_404(Sale.objects.filter(pk=pk))
    sale_items = SaleItem.objects.filter(sale=instance)
    context = {
        'title': 'Sale ' + str(instance.auto_id),
        'instance': instance,
        'sale_items': sale_items,

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
    return render(request, 'sales/sale.html', context)


def delete(request, pk):
    instance = get_object_or_404(Sale.objects.filter(pk=pk))
    sale_items = SaleItem.objects.filter(sale=instance)
    for p in sale_items:
        qty = p.qty
        update_stock(p.product.pk, qty, 'increase')
    instance.is_deleted = True
    instance.save()

    response_data = {
        "status" : "true",
        "title" : "Successfully Deleted",
        "message" : "Sale Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('sales:sales')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')