from django.urls import path, re_path
from livestream.views import upload, play, record

app_name = 'livestream'

urlpatterns = [
    path('', upload, name="index"),
    path('play/', play, name="play"),
    path('record/', record, name="record")
]