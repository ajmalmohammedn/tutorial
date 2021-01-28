from django.conf.urls import url
from rest_framework_simplejwt import views as jwt_views
import views

urlpatterns = [
    url(r'^token/$', views.UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/$', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]