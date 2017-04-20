from django.conf.urls import url
from .mainviews import views

urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='index'),
]