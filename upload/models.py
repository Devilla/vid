from django.db import models
from register.models import User
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    views = models.IntegerField(default=0)
    thumbsUp = models.IntegerField(default=0)
    thumbsDown = models.IntegerField(default=0)
    thumbNail = models.CharField(max_length=512)
    video = JSONField()
    duration = models.CharField(max_length=10)
    smoke = models.CharField(max_length=10)
    steem = models.CharField(max_length=10)
    whaleshares = models.CharField(max_length=10)
    valuation = models.CharField(max_length=10)
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    name = models.CharField(max_length=255, default='An apple a day keeps the doctor away')
    publish = models.BooleanField(default=False)
    nsfw = models.BooleanField(default=False)

class SteemVideo(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='steemVideos')
    permlink = models.CharField(max_length=1024, blank=True)
    author = models.CharField(max_length=256, blank=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    post_url = models.CharField(max_length=1024, blank=True)
    
class WhaleShareVideo(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='whaleVideos')
    permlink = models.CharField(max_length=1024, blank=True)
    author = models.CharField(max_length=256, blank=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    post_url = models.CharField(max_length=1024, blank=True)

class SmokeVideo(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='smokeVideos')
    permlink = models.CharField(max_length=1024, blank=True)
    author = models.CharField(max_length=256, blank=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    post_url = models.CharField(max_length=1024, blank=True)
