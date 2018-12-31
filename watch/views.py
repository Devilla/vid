from django.shortcuts import render, HttpResponse
from upload.models import Video, SteemVideo, WhaleShareVideo, SmokeVideo
from register.models import User
import demjson
from beem.comment import Comment

import json
# Create your views here.

def get_votes(s, author, permlink):
    acc = Comment("@{}/{}".format(author, permlink), steem_instance=s)

    upvotes = 0
    downvotes = 0

    for vote in acc.get_votes():
        if vote.rshares > 0:
            upvotes = upvotes + 1
        else:
            downvotes = downvotes + 1

    return upvotes, downvotes

def get_likes_dislikes(vid_id,user_details):
    total_likes = 0
    total_dislikes = 0

    try:
        steem = SteemVideo.objects.get(video_id=vid_id)
        steem_url = steem.post_url
        permalink = steem.permlink
        author = steem.author

        s = Steem(keys=[user_details.steem], nodes=["https://api.steemit.com", "https://rpc.buildteam.io"])
        s_upvote, s_downvote = get_votes(s, author, permalink)
        total_likes = total_likes + s_upvote
        total_dislikes = total_dislikes + s_downvote
    except Exception as e:
        print('Got Error: {}'.format(str(e)))


    try:
        whale = WhaleShareVideo.objects.get(video_id=vid_id)
        whale_url = whale.post_url
        permalink = whale.permlink
        author = whale.author

        wls = Steem(node=["https://rpc.whaleshares.io", "ws://188.166.99.136:8090", "ws://rpc.kennybll.com:8090"], keys=[user_details.whaleshare])
        w_upvote, w_downvote = get_votes(wls, author, permalink)

        total_likes = total_likes + w_upvote
        total_dislikes = total_dislikes + w_downvote
    except Exception as e: 
        print('Got Error: {}'.format(str(e)))


    try:
        smoke = SmokeVideo.objects.get(video_id=vid_id)
        smoke_url = smoke.post_url
        permalink = smoke.permlink
        author = smoke.author

        smk = Steem(node=['https://rpc.smoke.io/'], keys=[user_details.smoke], custom_chains={"SMOKE": {
            "chain_id": "1ce08345e61cd3bf91673a47fc507e7ed01550dab841fd9cdb0ab66ef576aaf0",
            "min_version": "0.0.0",
            "prefix": "SMK",
            "chain_assets": [
                {"asset": "STEEM", "symbol": "SMOKE", "precision": 3, "id": 1},
                {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
            ]
        }})

        sm_upvote, sm_downvote = get_votes(wls, author, permalink)
        total_likes = total_likes + sm_upvote
        total_dislikes = total_dislikes + sm_downvote

    except Exception as e: 
        print('Got Error: {}'.format(str(e)))

    return total_likes, total_dislikes

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

        user_details = User.objects.get(id=current.user_id)

        for each_video in featured:

            pay = 0


            steem_url = ""
            whale_url = ""
            smoke_url = ""

            total_likes, total_dislikes = get_likes_dislikes(each_video.vid_id, user_details)

            for each_res in resolution:
                if str(each_res) in each_video.video:
                    hash1 = demjson.decode(each_video.video)
                    each_video.featured = hash1[str(each_res)]
                    break   

        for each_video in recommend:
            
            pay = 0
            
            # try:
            #     steem = SteemVideo.objects.filter(video_id=each_video.id)
            #     steem_pay = SteemManager.get_payout(steem.post)
            #     pay = pay + steem_pay
            # except: 
            #     print('No Steem')

            # try:
            #     whale = WhaleShareVideo.objects.filter(video_id=each_video.id)
            #     whale_pay = WhalesharesManger.get_payout(whale.post)
            #     pay = pay + whale_pay
            # except: 
            #     print('No Whale')

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
        'user': user, 'count': count, 'steem_url': steem_url, 'smoke_url': smoke_url, 'whale_url': whale_url, 
        'total_likes': total_likes, 'total_dislikes': total_dislikes})    
