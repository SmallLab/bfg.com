from django.conf.urls import url
from . mainauth import views

urlpatterns = [
    url(r'^lfacebook/$', views.FacebookAuth.as_view(url='/'), name='lfacebook'),
    url(r'^bfgfacebook/$', views.getF, name='fget'),
]