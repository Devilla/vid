from django.urls import path, re_path
from single_channel.views import DetailView

app_name = 'single_channel'

urlpatterns = [
    path('<int:pk>/', DetailView, name="detail"),
]
