from django.urls import path, re_path
from logout.views import index

app_name = 'logout'

urlpatterns = [
    path('', index, name="logout"),
]
