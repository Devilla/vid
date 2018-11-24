from django.db import models
from register.models import User
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisement')
    ad = JSONField()

