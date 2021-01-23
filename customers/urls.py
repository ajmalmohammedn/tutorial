from django.conf.urls import url
import views


urlpatterns = [
	url(r'^create/$', views.create, name="create"),
	url(r'^edit/(?P<pk>.*)/$', views.edit, name="edit"),
	url(r'^$', views.customers, name="customers"),
	url(r'^customer/(?P<pk>.*)/$', views.customer, name="customer"),
	url(r'^delete/(?P<pk>.*)/$', views.delete, name="delete"),
]