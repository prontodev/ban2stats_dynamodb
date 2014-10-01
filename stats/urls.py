from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^/$', 'attack.views.get_stats', name='get_stats'),

)