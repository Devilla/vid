from django.db import models
from register.models import User
from django.contrib.postgres.fields import JSONField

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
    name = models.CharField(max_length=255, default='An apple a day keeps the doctor away')
    publish = models.BooleanField(default=False)
    nsfw = models.BooleanField(default=False)
