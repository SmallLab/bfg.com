from django.conf.urls import url
from . mainviews import views

urlpatterns = [
   url(r'^addsentense/$', views.AddNewSentenseView.as_view(), name='addsentense'),

]