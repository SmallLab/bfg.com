from django.conf.urls import url
from . mainauth import views

urlpatterns = [
    url(r'^lfacebook/$', views.FacebookAuth.as_view(url='http://localhost:8000/user/privateoffice/sent'), name='lfacebook'),
]