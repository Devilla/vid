from django.urls import path, re_path
from livestream.views import livefe

app_name = 'livestream'

urlpatterns = [
    path('', livefe, name="index"),
]