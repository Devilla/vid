from django.db import models
from register.models import User
from upload.models import Video
# Create your models here.

class commentsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='commented_video')
    comment = models.TextField()
    userName = models.CharField(max_length=100, default='')
    comment_likes = models.IntegerField(default=0)
    comment_replies = models.IntegerField(default=0)
    parent_comment_id = models.IntegerField(default=0)

class CommentReplies(models.Model):
    comment = models.ForeignKey(commentsModel, on_delete=models.CASCADE, related_name='comment_reply')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_user')
    userName = models.CharField(max_length=512)
    reply = models.TextField(default ='')