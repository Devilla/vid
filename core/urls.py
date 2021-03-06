from django.urls import path, re_path, include
from django.conf.urls import url
from core.views import index, videoLike, videoDisLike, about, light, help, nsfw_status, followChannel, singleTagVideos, changeAutoplay, commentLike, commentDisLike

app_name = 'core'

urlpatterns = [
    path('', index, name="index"),
    url(r'^like/$', videoLike, name="like"),
    url(r'^dislike/$', videoDisLike, name="dislike"),
    url(r'^commentLike/$', commentLike, name="commentlike"),
    url(r'^commentDislike/$', commentDisLike, name="commentdislike"),
    url(r'^about/$', about, name="about"),
    url(r'^help/$', help, name="help"),
    url(r'^nsfw_status/$', nsfw_status, name="nsfw_status"),
    url(r'^light/$', light, name="light_status"),
    url(r'^followUnfollow/$',followChannel, name='followChannel'),
    url(r'^autoplay/$',changeAutoplay, name='changeAutoplay'),
    path('tagged/<str:tag>/',singleTagVideos, name='singleTagVideos'),
]
