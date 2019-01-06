from django.db import models
from register.models import User
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
import os
import uuid

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("files", filename)


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path, null=True)

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    views = models.IntegerField(default=0)
    thumbsUp = models.IntegerField(default=0)
    thumbsDown = models.IntegerField(default=0)
    thumbNail = models.CharField(max_length=512)
    video = JSONField()
    duration = models.CharField(max_length=10)
    tags = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True)
    language_choices = [(1,'English'),(2,'Chinese'), (3,'Spanish'), (4,'German')]
    language = models.CharField(max_length =20, choices=language_choices, default='1')
    smoke = models.FloatField(default=0.0)
    steem = models.FloatField(default=0.0)
    whaleshares = models.FloatField(default=0.0)
    total_earning = models.FloatField(default=0.0)
    valuation = models.CharField(max_length=10)
    #tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)
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
