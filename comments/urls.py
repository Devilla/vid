from django.urls import path, re_path
from .views import userComments, commentReplies

app_name = 'comments'

urlpatterns = [
    path('addComment/', userComments, name="addComment"),
    path('commentReplies/', commentReplies, name="commentReplies"),

]
