from django.urls import path, re_path
from django.conf.urls import url
from core.views import index, videoLike

app_name = 'core'

urlpatterns = [
    path('', index, name="index"),
    url(r'^video/addlike/$', videoLike, name='add_like'),
]
