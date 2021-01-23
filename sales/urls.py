from django.conf.urls import url
import views


urlpatterns = [
	url(r'^create/$', views.create, name="create"),
	url(r'^edit/(?P<pk>.*)/$', views.edit, name="edit"),
	url(r'^$', views.sales, name="sales"),
	url(r'^sale/(?P<pk>.*)/$', views.sale, name="sale"),
	url(r'^delete/(?P<pk>.*)/$', views.delete, name="delete"),
]