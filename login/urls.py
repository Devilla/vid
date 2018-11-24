from django.urls import path, re_path
from login.views import index

app_name = 'login'

urlpatterns = [
    path('', index, name="login"),
]
