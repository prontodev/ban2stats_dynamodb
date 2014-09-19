from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^new/$', 'attack.views.add_attack', name='add_attack'),

)
