from django.urls import path, include
from .views import index

app_name = 'ad'
urlpatterns = [
    path('', index, name="index"),
]