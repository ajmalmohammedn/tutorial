from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from main.functions import get_auto_id, get_a_id, generate_form_errors
from django.contrib.auth.decorators import login_required
from  main.decorators import ajax_required
from django.db.models import Q
import json
import datetime
from customers.models import Customer
from customers.forms import CustomerForm
from dal import autocomplete


class CustomerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Customer.objects.none()

        items = Customer.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query) | Q(address__icontains=query))

        return items


@login_required
def create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updator = request.user
            data.auto_id = get_auto_id(Customer)
            data.save()

            return HttpResponseRedirect(reverse('customers:customer', kwargs={"pk": data.pk}))
        else:
            form = CustomerForm(request.POST)
            context = {
                'form': form,
                'title': 'Create Customer',
                'redirect': True,
                'url': reverse('customers:create'),

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
            return render(request, 'customers/entry.html', context)
    else:
        form = CustomerForm(initial = {
            'name': 'Ajmal Muhammed',
            'email': 'ajmalmuhammed.talrop@gmail.com'
            })
        context = {
            'form': form,
            'title': 'Create Customer',
            'redirect': True,
            'url': reverse('customers:create'),

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
        return render(request, 'customers/entry.html', context)


@login_required
def edit(request, pk):
    instance = get_object_or_404(Customer.objects.filter(pk=pk))
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updator = request.user
            data.date_updated = datetime.datetime.now()
            data.save()

            return HttpResponseRedirect(reverse('customers:customer', kwargs={"pk": data.pk}))
        else:
            form = CustomerForm(instance=instance)
            context = {
                'form': form,
                'title': 'Create Customer',
                'redirect': True,
                'url': reverse('customers:edit', kwargs={'pk':instance.pk}),

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
            return render(request, 'customers/entry.html', context)
    else:
        form = CustomerForm(instance=instance)
        context = {
            'form': form,
            'title': 'Create Customer',
            'redirect': True,
            'url': reverse('customers:edit', kwargs={'pk':instance.pk}),

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
        return render(request, 'customers/entry.html', context)



@login_required
def customers(request):
    instances = Customer.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query) | Q(address__icontains=query)  )

    context = {
        'title': 'Customers',
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
    return render(request, 'customers/customers.html', context)


@login_required
def customer(request, pk):
    instance = get_object_or_404(Customer.objects.filter(pk=pk))
    context = {
        'title': 'Customer - ' + instance.name,
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
    return render(request, 'customers/customer.html', context)


@login_required
@ajax_required
def delete(request, pk):
    Customer.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "true",
        "title" : "Successfully Deleted",
        "message" : "Customer Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('customers:customers')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def get_customer(request):
    pk = request.GET.get('id')
    if Customer.objects.filter(pk=pk).exists():
        customer = Customer.objects.get(pk=pk)

        response_data = {
            'status': 'true',
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'address': customer.address,
            'pk': str(customer.pk)
        }
    else:
        response_data = {
            'status': 'false',
            'message': 'Customer not exist'
        }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
