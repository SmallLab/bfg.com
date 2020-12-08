"""bfg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import LogoutView


from django.conf import settings
from django.conf.urls.static import static

from mainbfg.views import LoginUser, RegistrationUser


urlpatterns = [
    url(r'^', include('mainbfg.urls')),
    url(r'^authcocial/', include('smyauth.urls')),
    url(r'^user/', include('userswork.urls')),
    url(r'^login/$', LoginUser, name='login'),
    url(r'^registrations/$', RegistrationUser, name='reristrations'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^admin/clearcache/', include('clearcache.urls')),
    url(r'^admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
