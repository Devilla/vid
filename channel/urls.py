from django.urls import path, re_path, include
from django.conf.urls import url
from channel.views import mychannel
app_name = 'channel'

urlpatterns = [
    url(r'^mychannel/$', mychannel, name="mychannel"),
]
