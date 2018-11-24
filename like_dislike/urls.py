from django.urls import path, re_path
from like_dislike.views import like, dislike

app_name = 'activity'

urlpatterns = [    
    re_path(r'^like/', like, name="like"),
    re_path(r'^dislike/', dislike, name="dislike"),    
]
