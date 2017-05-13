from django.conf.urls import url
from . mainauth import views

urlpatterns = [
    url(r'^lfacebook/$', views.FacebookAuth.as_view(), name='lfacebook'),
]