from django.urls import path, re_path
from register.views import index, update

app_name = 'register'

urlpatterns = [
    path('', index, name="register"),
    path('update/', update, name="update"),
]
