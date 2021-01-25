from django.conf.urls import url
import views
from customers.views import CustomerAutocomplete


urlpatterns = [
	url(r'^customer-autocomplete/$',CustomerAutocomplete.as_view(),name='customer_autocomplete'),
	url(r'^create/$', views.create, name="create"),
	url(r'^edit/(?P<pk>.*)/$', views.edit, name="edit"),
	url(r'^$', views.customers, name="customers"),
	url(r'^customer/(?P<pk>.*)/$', views.customer, name="customer"),
	url(r'^delete/(?P<pk>.*)/$', views.delete, name="delete"),
]