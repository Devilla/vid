from django.db import models

# Create your models here.
class AssetPrice(models.Model):
    curr_time = models.DateTimeField(auto_now_add=True)
    steem_price = models.FloatField(default=0.269)
    smoke_price = models.FloatField(default=0.05)
    whaleshare_price = models.FloatField(default=0.1)