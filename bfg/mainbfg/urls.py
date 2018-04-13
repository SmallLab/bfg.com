from django.conf.urls import url
from . mainviews import views
from . import views as vv

urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='index'),
    url(r'^categories/(?P<link_name>[a-z0-9-]+)/(?:type/(?P<type>\w+)/)?(?:page/(?P<page>\d+)/)?$', views.CategoryPage.as_view(),
        name='categorypage'),
    url(r'^filtersent/(?:page/(?P<page>\d+)/)?$', views.FilterSentences.as_view(), name='filtersent'),
    url(r'^alltop/(?:page/(?P<page>\d+)/)?$', views.AllTop.as_view(), name='alltop'),
    url(r'^sentence/.+_(?P<slug>.+)/$', views.ViewSentence.as_view(), name='detail'),
    url(r'^sentence/showphone/$', views.ShowPhone.as_view(), name='showphone'),
    # url(r'^registrations/$', vv.RegistrationUser, name='reristrations'),
]