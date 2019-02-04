from django.contrib import admin
from django.urls import path, re_path
from watch.views import index, adView
from django.conf.urls import url

app_name = 'watch'

urlpatterns = [    
    re_path(r'^(?P<video_hash>[\w-]+)/(?P<video_id>[\w-]+)/$', index, name="index"),
    url(r'^adView/$', adView, name="adView"),
    
]
