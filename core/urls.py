from django.urls import path, re_path, include
from django.conf.urls import url
from core.views import index, videoLike, videoDisLike

app_name = 'core'

urlpatterns = [
    path('', index, name="index"),
    url(r'^like/$', videoLike, name="like"),
    url(r'^dislike/$', videoDisLike, name="dislike"),
]
