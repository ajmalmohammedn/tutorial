from django.conf.urls import url
import views


urlpatterns = [
	url(r'^create/$', views.create, name="create"),
	url(r'^edit/(?P<pk>.*)/$', views.edit, name="edit"),
	url(r'^$', views.products, name="products"),
	url(r'^product/(?P<pk>.*)/$', views.product, name="product"),
	url(r'^delete/(?P<pk>.*)/$', views.delete, name="delete"),
]