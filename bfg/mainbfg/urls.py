from django.conf.urls import url
from . mainviews import views
from . import views as vv

urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='index'),
    url(r'^registrations/$', vv.RegistrationUser, name='reristrations')
]