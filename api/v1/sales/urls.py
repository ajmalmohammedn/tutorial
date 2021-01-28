from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.sales, name="sales"),
    url(r'^sale/(?P<pk>.*)/$', views.sale, name="sale"),
]