from django.shortcuts import render, HttpResponse
from upload.models import Video
from register.models import User
import demjson

import json
# Create your views here.


def index(request, video_hash, video_id):
    current = Video.objects.get(id=video_id)

    hash = json.loads(current.video)
    resolution = [2160, 1440, 1080, 720, 480, 360, 240  , 144]

    isVideo = False

    for each_res in resolution:
        if str(each_res) in current.video:
            if hash[str(each_res)] == video_hash:
                isVideo = True
                break  
        
    if isVideo == True:
        views = current.views
        current.views = views+1
        current.save()

        featured = Video.objects.all().order_by('-id')[:1]
        recommend = Video.objects.all().order_by('-views')[:1]

        user = User.objects.get(id=current.user_id)
        count = Video.objects.filter(user_id=current.user_id).count()

        bestHash_Featured = []
        bestHash_Recomended = []

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
                    hash1 = demjson.decode(each_video.video)
                    each_video.featured = hash1[str(each_res)]
                    break   

        for each_video in recommend:
            
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
                    hash1 = demjson.decode(each_video.video)
                    each_video.recommend = hash1[str(each_res)]
                    break   

        
        dump = json.dumps(hash)
        
        video_content = ''

        for quality, this_hash in hash.items():
            video_content = video_content + '{\n\t src: \'https://gateway.ipfs.io/ipfs/' + this_hash + '\',\n\t type: \'video/mp4\',\n\t size: ' + quality + ',\n},\n' 
        
                    
        return render(request, "watch/base.html", {'video_hash': hash, 'cont': video_content,
        'latest': featured, 'recommended': recommend, 'current': current,
        'user': user, 'count': count })
    
