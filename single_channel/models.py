from django.db import models
from register.models import User

# Create your models here.
class followersModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    total_followers = models.IntegerField(default=0)
