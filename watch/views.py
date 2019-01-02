from django.shortcuts import render, HttpResponse
from upload.models import Video, SteemVideo, WhaleShareVideo, SmokeVideo
from register.models import User
import demjson
from like_dislike.models import Activity
from beem.comment import Comment
from beem import Steem

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

def get_likes_dislikes(vid_id):
    total_likes = 0
    total_dislikes = 0

    steem_url = ""
    whale_url = ""
    smoke_url = ""

    try:
        steem = SteemVideo.objects.get(video_id=vid_id)
        steem_url = steem.post_url
        permalink = steem.permlink
        author = steem.author

        s = Steem(nodes=["https://api.steemit.com", "https://rpc.buildteam.io"])
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

        wls = Steem(node=["https://rpc.whaleshares.io", "ws://188.166.99.136:8090", "ws://rpc.kennybll.com:8090"])
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

        smk = Steem(node=['https://rpc.smoke.io/'], custom_chains={"SMOKE": {
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

    print("Likes: {} Dislikes: {}".format(total_likes, total_dislikes))

    return steem_url, smoke_url, whale_url, total_likes, total_dislikes

def index(request, video_hash, video_id):
    current = Video.objects.get(id=video_id)
    steem_url, smoke_url, whale_url, total_likes, total_dislikes = get_likes_dislikes(current.id)

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
            for each_res in resolution:
                if str(each_res) in each_video.video:
                    hash1 = demjson.decode(each_video.video)
                    each_video.featured = hash1[str(each_res)]
                    break   

        for each_video in recommend:
            for each_res in resolution:
                if str(each_res) in each_video.video:
                    hash1 = demjson.decode(each_video.video)
                    each_video.recommend = hash1[str(each_res)]
                    break   

        
        dump = json.dumps(hash)
        
        video_content = ''

        for quality, this_hash in hash.items():
            video_content = video_content + '{\n\t src: \'https://gateway.ipfs.io/ipfs/' + this_hash + '\',\n\t type: \'video/mp4\',\n\t size: ' + quality + ',\n},\n' 
        
        chkLike, chkDislike = likedordisliked (request, request.user.id, video_id)

        return render(request, "watch/base.html", {'video_hash': hash, 'cont': video_content,
        'latest': featured, 'recommended': recommend, 'current': current,
        'user': user, 'count': count, 'steem_url': steem_url, 'smoke_url': smoke_url, 'whale_url': whale_url, 'chkLike': chkLike, 'chkDislike':chkDislike,
        'total_likes': total_likes, 'total_dislikes': total_dislikes})
    

def likedordisliked (request, user_id, video_id):
    if request.user.is_authenticated:
            likeDislike = Activity.objects.filter(user_id=user_id, video_id = video_id).exists()
            if likeDislike == True:
                checkLikeDislike = Activity.objects.get(user_id=user_id, video_id = video_id)
                chkLike = checkLikeDislike.thumbsUp
                chkDislike = checkLikeDislike.thumbsDown
                return chkLike, chkDislike
            else:
                return False ,False