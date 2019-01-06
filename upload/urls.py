from django.contrib import admin
from django.urls import path, re_path
from upload.views import index, after_clicked, ajax_upload

app_name = 'upload'

urlpatterns = [
    path('', index, name="index"),
    re_path(r'^after_clicked', after_clicked, name='after_clicked'),
    re_path(r'^ajax_upload/$', ajax_upload, name='ajax_upload'),
]