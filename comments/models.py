from threadedcomments.models import ThreadedComment
from django.db import models

class CustomThreadedComment(ThreadedComment):
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)