from django.conf.urls import url
from . mainviews import views

urlpatterns = [
   url(r'^addsentense/$', views.CreateNewSentence.as_view(), name='showform'),
   url(r'^createsentence/$', views.CreateNewSentence.as_view(), name='createsentence'),
   url(r'^privateoffice/(?P<tab>[\w]*)/?$', views.PrivateOfficeView.as_view(), name='privateoffice'),
   url(r'^privateoffice/delete/(?P<pk>\d+)/$', views.PODeleteSentenceView.as_view(), name='deletesent'),
   url(r'^privateoffice/deactive/(?P<pk>\d+)/$', views.PODeactiveSentenceView.as_view(), name='deactivesent'),
   url(r'^privateoffice/activete/(?P<pk>\d+)/$', views.POActiveSentenceView.as_view(), name='activatesent'),
   url(r'^privateoffice/edit/(?P<pk>\d+)/$', views.POEditSentenceView.as_view(), name='editsent')
]