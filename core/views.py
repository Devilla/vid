from django.shortcuts import render
from upload.models import Video, SteemVideo, WhaleShareVideo
from register.models import User
import json
import demjson
from blockchain_manager.manager import SteemManager, WhalesharesManger

# Create your views here.
def index(request):
    
    featured = Video.objects.all().order_by('-id')[:8]
    trending = Video.objects.all().order_by('-views')[:8]
    channels = User.objects.all().order_by('-id')[:11]
    
    bestHash_Featured = []
    bestHash_Trending = []

    resolution = [2160, 1440, 1080, 720, 480, 360, 240  , 144]

    for each_video in featured:
        
        pay = 0
        try:
            steem = SteemVideo.objects.filter(video_id=each_video.id)
            steem_pay = SteemManager.get_payout(steem.post)
            pay = pay + steem_pay
        except: 
            print('No Steem')

        try:
            whale = WhaleShareVideo.objects.filter(video_id=each_video.id)
            whale_pay = WhalesharesManger.get_payout(whale.post)
            pay = pay + whale_pay
        except: 
            print('No Whale')

        each_video.money = pay

        for each_res in resolution:
            if str(each_res) in each_video.video:
                hash = demjson.decode(each_video.video)
                each_video.bestHash_Featured = hash[str(each_res)]
                break   

    for each_videot in trending:
        
        pay = 0
        try:
            steem = SteemVideo.objects.filter(video_id=each_videot.id)
            steem_pay = SteemManager.get_payout(steem.post)
            pay = pay + steem_pay
        except: 
            print('No Steem')

        try:
            whale = WhaleShareVideo.objects.filter(video_id=each_videot.id)
            whale_pay = WhalesharesManger.get_payout(whale.post)
            pay = pay + whale_pay
        except: 
            print('No Whale')

        each_videot.money = pay

        for each_res in resolution:
            if str(each_res) in each_videot.video:
                hasht = demjson.decode(each_videot.video)
                each_videot.bestHash_Trending = hasht[str(each_res)]
                break   
    
    for each_channel in channels:
        try:
            video = Video.objects.filter(user_id=each_channel.id).count()
            each_channel.count = video
        except:
            each_channel.count = 0
            
    return render(request, "core/home.html", {'instance': featured, 'trend': trending, 
                                                  'subscription': channels })
