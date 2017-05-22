from django.conf.urls import url
from . mainviews import views

urlpatterns = [
   url(r'^addsentense/$', views.ShowFormSentenseView.as_view(), name='showform'),
   url(r'^createsentence/$', views.CreateNewSentence.as_view(), name='createsentence')

]