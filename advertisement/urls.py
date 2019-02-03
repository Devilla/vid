from django.urls import path, include
from .views import index,pay
from django.conf.urls import url


app_name = 'ad'
urlpatterns = [
    path('', index, name="index"),
    url(r'^pay/$', pay, name="pay"),
]