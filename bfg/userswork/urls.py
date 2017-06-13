from django.conf.urls import url
from . mainviews import views

urlpatterns = [
   url(r'^addsentense/$', views.ShowFormSentenseView.as_view(), name='showform'),
   url(r'^createsentence/$', views.CreateNewSentence.as_view(), name='createsentence'),
   url(r'^privateoffice/(?P<tab>[\w]*)/?$', views.PrivateOfficeView.as_view(), name='privateoffice'),
   url(r'^privateoffice/delete/(?P<pk>\d+)/$', views.PODeleteSentenceView.as_view(), name='deletesent')
]