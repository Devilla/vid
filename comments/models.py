from threadedcomments.models import ThreadedComment
from django.db import models

class CustomThreadedComment(ThreadedComment):
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    steem_id = models.CharField(max_length=1024, default='', blank=True)
    smoke_id = models.CharField(max_length=1024, default='', blank=True)
    whaleshare_id = models.CharField(max_length=1024, default='', blank=True)