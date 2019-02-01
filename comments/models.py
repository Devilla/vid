from threadedcomments.models import ThreadedComment
from django.db import models
from register.models import User

class CustomThreadedComment(ThreadedComment):
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    steem_id = models.CharField(max_length=1024, default='', blank=True)
    smoke_id = models.CharField(max_length=1024, default='', blank=True)
    whaleshare_id = models.CharField(max_length=1024, default='', blank=True)

class commentLDinfo(models.Model):
    LDuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_user')
    LDcomment = models.ForeignKey(CustomThreadedComment, on_delete=models.CASCADE, related_name='main_comment')
    like = models.BooleanField(default=False)
    steem_like = models.BooleanField(default=False)
    smoke_like = models.BooleanField(default=False)
    whaleshare_like = models.BooleanField(default=False)

    dislike = models.BooleanField(default=False)
    steem_dislike = models.BooleanField(default=False)
    smoke_dislike = models.BooleanField(default=False)
    whaleshare_dislike = models.BooleanField(default=False)