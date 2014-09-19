from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'ban2stats.views.home', name='home'),

    url(r'^attack/', include('attack.urls')),
)
