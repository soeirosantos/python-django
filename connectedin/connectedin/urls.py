from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('perfis.urls')),
    url(r'^', include('usuarios.urls')),
    url(r'^admin/', include(admin.site.urls)),
)