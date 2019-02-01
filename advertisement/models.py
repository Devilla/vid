from django.db import models
from register.models import User
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisement')
    ad_title = models.CharField(max_length=255)
    ad_banner = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    currently_played = models.IntegerField(default=0)
    total_plays = models.IntegerField(default=0)
    targeted_tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)