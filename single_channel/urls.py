from django.urls import path, re_path
from single_channel.views import mychannel
from django.conf.urls import url

app_name = 'single_channel'

urlpatterns = [
    url(r'^mychannel/$', mychannel, name="mychannel"),
]
