from django.urls import path, re_path
from single_channel.views import mychannel, myprofile, steem_blockchain, smoke_blockchain, whale_blockchain


app_name = 'single_channel'

urlpatterns = [
    path('<int:pk>/', mychannel, name="mychannel"),
    path('myprofile/<int:pk>/', myprofile, name="myprofile"),
    path('steemUpdate/',steem_blockchain, name='steemUpdate'),
    path('smokeUpdate/',smoke_blockchain, name='smokeUpdate'),
    path('whaleUpdate/',whale_blockchain, name='whaleUpdate'),
]
