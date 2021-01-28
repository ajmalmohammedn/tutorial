from django.conf.urls import url
import views


urlpatterns = [
    url(r'^create/$', views.create_customer, name="create_customer"),
    url(r'^edit/(?P<pk>.*)/$', views.edit_customer, name="edit_customer"),
    url(r'^$', views.customers, name="customers"),
    url(r'^customer/(?P<pk>.*)/$', views.customer, name="customer"),
]