from django.db import models
from register.models import User
from upload.models import Video

# Create your models here.
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity')
    thumbsUp = models.BooleanField(default=False)
    thumbsDown = models.BooleanField(default=False)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # id_unique = models.IntegerField(unique=True, serialize=True, default=1)


    # def __str__(self):
    #     return self.id_unique
