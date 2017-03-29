from django.conf.urls import url

#from . import views
from .mainviews import index

urlpatterns = [
    url(r'^$', index.index, name='index'),
]