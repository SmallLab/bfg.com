from django.conf.urls import url
from . mainviews import views
from . import views as vv

urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='index'),
    url(r'^sentence/.+_(?P<slug>.+)/$', views.ViewSentence.as_view(), name='detail'),
    url(r'^sentence/showphone/$', views.ShowPhone.as_view(), name='showphone'),
    url(r'^registrations/$', vv.RegistrationUser, name='reristrations'),

]