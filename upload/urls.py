from django.contrib import admin
from django.urls import path, re_path
from upload.views import index, info

app_name = 'upload'

urlpatterns = [
    path('', index, name="index"),
    path('info/', info, name="info"),
]