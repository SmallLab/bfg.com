from django.conf.urls import url

#from . import views
from .mainviews import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]