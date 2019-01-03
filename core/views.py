from django.shortcuts import render,redirect 
from upload.models import Video, SteemVideo, WhaleShareVideo, SmokeVideo
from like_dislike.models import Activity
from register.models import User
from django.http import JsonResponse
from django.http import HttpResponse
from threading import Thread

import json
import demjson
from core.models import AssetPrice
from datetime import datetime
import pytz
import requests
import json

from beem import Steem
from beem.comment import Comment

import schedule
import time

def get_payout(s, author, permlink):
    try:
        acc = Comment("@{}/{}".format(author, permlink), steem_instance=s)
        payout = float(str(acc.reward).split()[0])
    except Exception as e:
        payout = 0.00
    
    return payout

def upvote(s, post_author, permlink, voter):
    acc = Comment("@{}/{}".format(post_author, permlink), steem_instance=s)
    votes = acc.upvote(voter=voter)

def downvote(s, post_author, permlink, voter):
    acc = Comment("@{}/{}".format(post_author, permlink), steem_instance=s)
    votes = acc.downvote(voter=voter)


s_no_auth = Steem(nodes=["https://api.steemit.com", "https://rpc.buildteam.io"])
w_no_auth = Steem(node=["https://rpc.whaleshares.io", "ws://188.166.99.136:8090", "ws://rpc.kennybll.com:8090"])
sm_no_auth = Steem(node=['https://rpc.smoke.io/'], custom_chains={"SMOKE": {
                    "chain_id": "1ce08345e61cd3bf91673a47fc507e7ed01550dab841fd9cdb0ab66ef576aaf0",
                    "min_version": "0.0.0",
                    "prefix": "SMK",
                    "chain_assets": [
                        {"asset": "STEEM", "symbol": "SMOKE", "precision": 3, "id": 1},
                        {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
                    ]
                }})

def update_prices():
    '''
    Gets the price for steem, smoke and whaleshares
    '''

    print("Updating price")
    steem_price = 0
    smoke_price = 0
    whaleshare_price = 0

    latest_price = AssetPrice.objects.all().order_by('-curr_time')[:1][0]
    steem_price = latest_price.steem_price
    smoke_price = latest_price.smoke_price
    whaleshare_price = latest_price.whaleshare_price

    try:
        r=requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=STEEM,USD", headers={"X-CMC_PRO_API_KEY":"030f8706-dc8a-442b-82bb-8824eecf4e6e"}, timeout=1)
        res = json.loads(r.text)
        p = float(res['data']['STEEM']['quote']['USD']['price'])

        if p > 0:
            steem_price = p
    except:
        pass

    try:
        r=requests.get("https://cryptofresh.com/api/asset/markets?asset=SMOKE", timeout=0.1)
        res = json.loads(r.text)
        p = float(res['USD']['price'])

        if p > 0:
            smoke_price = p
    except:
        pass

    try:
        r=requests.get("https://cryptofresh.com/api/asset/markets?asset=WHALESHARE")
        res = json.loads(r.text)
        p = float(res['USD']['price'])

        if p > 0:
            whaleshare_price = p
    except:
        pass

    a = AssetPrice(steem_price=steem_price, smoke_price=smoke_price, whaleshare_price=whaleshare_price)
    a.save()

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

def update_single_earning_like_dislike(video_id):

    total_likes = 0
    total_dislikes = 0

    total_earning = 0.0

    latest_price = AssetPrice.objects.all().order_by('-curr_time')[:1][0]
    steem_price = latest_price.steem_price
    smoke_price = latest_price.smoke_price
    whaleshare_price = latest_price.whaleshare_price

    video_details = Video.objects.get(id=video_id)

    try:
        single_val = SteemVideo.objects.get(video_id=video_id)

        permlink = single_val.permlink
        author = single_val.author

        try:
            s_upvote, s_downvote = get_votes(s_no_auth, author, permlink)
            total_likes = total_likes + s_upvote
            total_dislikes = total_dislikes + s_downvote
        except Exception as e:
            print("Steem upvote error: {}".format(str(e)))

        steem_payout = get_payout(s_no_auth, author, permlink) * steem_price
        total_earning = total_earning + steem_payout

        video_details.steem = steem_payout

        print("Updated")
    except Exception as e: 
        print('No Steem. Error is {}'.format(str(e)))

    try:
        single_val = SmokeVideo.objects.get(video_id=video_id)

        permlink = single_val.permlink
        author = single_val.author

        try:
            sm_upvote, sm_downvote = get_votes(sm_no_auth, author, permlink)
            total_likes = total_likes + sm_upvote
            total_dislikes = total_dislikes + sm_downvote
        except Exception as e:
            print("Smoke upvote error: {}".format(str(e)))

        smoke_payout = get_payout(sm_no_auth, author, permlink) * smoke_price
        total_earning = total_earning + smoke_payout
        
        video_details.smoke = smoke_payout

        print("Updated")
    except Exception as e: 
        print('No Smoke. Error is {}'.format(str(e)))

    try:
        single_val = WhaleShareVideo.objects.get(video_id=video_id)

        permlink = single_val.permlink
        author = single_val.author

        try:
            w_upvote, w_downvote = get_votes(w_no_auth, author, permlink)
            total_likes = total_likes + w_upvote
            total_dislikes = total_dislikes + w_downvote
        except Exception as e:
            print("Whaleshare upvote error: {}".format(str(e)))

        whale_payout = get_payout(w_no_auth, author, permlink) * whaleshare_price
        total_earning = total_earning + whale_payout
        
        video_details.whaleshares = whale_payout

        print("Updated")
    except Exception as e: 
        print('No Whaleshares. Error is {}'.format(str(e)))

    video_details.total_earning = total_earning
    video_details.thumbsUp =  total_likes
    video_details.thumbsDown = total_dislikes
    video_details.save()

def update_likes_payout():
    '''
    Updates all payouts and likes
    '''
    get_videos = Video.objects.all()
    
    for all_videos in get_videos:
        video_id = all_videos.id
        update_single_earning_like_dislike(video_id)


def keep_updating():
    schedule.every(10).minutes.do(update_prices)

    while True:
        time.sleep(1)
        schedule.run_pending()

# Create your views here
def index(request):

    thread = Thread(target = keep_updating)
    thread.start()

    if (len(AssetPrice.objects.all())) == 0:
        AssetPrice().save()

    update_likes_payout()

    featured = Video.objects.all().order_by('-id')[:8]
    trending = Video.objects.all().order_by('-views')[:8]
    channels = User.objects.all().order_by('-id')[:11]
    
    bestHash_Featured = []
    bestHash_Trending = []

    resolution = [2160, 1440, 1080, 720, 480, 360, 240  , 144]

    for each_video in featured:
        for each_res in resolution:
            if str(each_res) in each_video.video:
                hash = demjson.decode(each_video.video)
                each_video.bestHash_Featured = hash[str(each_res)]
                break   

    for each_videot in trending:
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
            channels.remove(each_channel)
    

    return render(request, "core/home.html", {'instance': featured, 'trend': trending, 'subscription': channels})

def perform_likes_dislike(account_details, type=1):
    '''
    type(int):
    1 to like, other for dislike
    '''
    for key in account_details:
        
        try:
            if 'key' in account_details[key]:
                if key == 'steem':
                    s = Steem(keys=[account_details[key]['key']], nodes=["https://api.steemit.com", "https://rpc.buildteam.io"])
                elif key == 'smoke':
                    s = Steem(keys=[account_details[key]['key']], node=['https://rpc.smoke.io/'], custom_chains={"SMOKE": {
                        "chain_id": "1ce08345e61cd3bf91673a47fc507e7ed01550dab841fd9cdb0ab66ef576aaf0",
                        "min_version": "0.0.0",
                        "prefix": "SMK",
                        "chain_assets": [
                            {"asset": "STEEM", "symbol": "SMOKE", "precision": 3, "id": 1},
                            {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
                        ]
                    }})
                else:
                    s = Steem(keys=[account_details[key]['key']], node=["ws://188.166.99.136:8090", "ws://rpc.kennybll.com:8090","https://rpc.whaleshares.io"])

                if type==1:
                    upvote(s, account_details[key]['author'], account_details[key]['permlink'], account_details[key]['username'])
                else:
                    downvote(s, account_details[key]['author'], account_details[key]['permlink'], account_details[key]['username'])
        except Exception as e:
            print("Error while like/dislike: {}".format(str(e)))

def videoLike(request):
    if request.method == "POST":
        if request.user.is_authenticated == True:
            videoid = request.POST.get("likevideoID")
            user_id = request.user.id
            user_details = User.objects.get(id=user_id)

            alreadyLiked = False
            alreadyDisliked = False

            try:
                dislikeActivity = Activity.objects.filter(user_id=user_id, video_id = videoid).exists()
                if dislikeActivity == False:
                    addDislike = Activity()
                    addDislike.thumbsUp = False
                    addDislike.thumbsDown = True
                    addDislike.user_id = user_id
                    addDislike.video_id = videoid
                    addDislike.save()
                elif dislikeActivity == True:
                    addDislike = Activity.objects.get(user_id=user_id, video_id = videoid)
                    if addDislike.thumbsUp == True and addDislike.thumbsDown == False:
                        addDislike.thumbsUp = False
                        addDislike.thumbsDown = True
                        addDislike.save()
                    else:
                        alreadyDisliked = True
            except:
                pass

            try:
                likeActivity = Activity.objects.filter(user_id=user_id, video_id = videoid).exists()
                if likeActivity == False:
                    addLike = Activity()
                    addLike.thumbsUp = True
                    addLike.thumbsDown = False
                    addLike.user_id = user_id
                    addLike.video_id = videoid
                    addLike.save()
                elif likeActivity == True:
                    addLike = Activity.objects.get(user_id=user_id, video_id = videoid)
                    if addLike.thumbsUp == False and addLike.thumbsDown == True:
                        addLike.thumbsUp = True
                        addLike.thumbsDown = False
                        addLike.save()
                    else:
                        alreadyLiked = True
            except:
                pass

            videoDetails = Video.objects.get(id=videoid)
            totalLike = videoDetails.thumbsUp
            totalDislike = videoDetails.thumbsDown

            account_details = {}

            try:
                if len(user_details.steem) >=6:
                    account_details['steem'] = {}
                    steem_details = SteemVideo.objects.get(video_id=videoid)
                    account_details['steem']['key'] = user_details.steem
                    account_details['steem']['author'] = steem_details.author
                    account_details['steem']['permlink'] = steem_details.permlink
            except:
                pass

            try:
                if len(user_details.smoke) >=6:
                    account_details['smoke'] = {}
                    smoke_details = SmokeVideo.objects.get(video_id=videoid)
                    account_details['smoke']['key'] = user_details.smoke
                    account_details['smoke']['author'] = smoke_details.author
                    account_details['smoke']['permlink'] = smoke_details.permlink
            except:
                pass

            try:
                if len(user_details.whaleshare) >=6:
                    account_details['whaleshare'] = {}
                    whaleshare_details = WhaleShareVideo.objects.get(video_id=videoid)
                    account_details['whaleshare']['key'] = user_details.whaleshare
                    account_details['whaleshare']['author'] = whaleshare_details.author
                    account_details['whaleshare']['permlink'] = whaleshare_details.permlink
            except:
                pass

            print(account_details)

            if alreadyLiked == False:  
                like_thread = Thread(target=perform_likes_dislike, args=(account_details, 1,))    
                like_thread.start()

                try:
                    totalLike = videoDetails.thumbsUp + len(account_details)
                    videoDetails.thumbsUp = totalLike

                    if alreadyDisliked == True:
                        totalDislike = totalDislike - len(account_details)

                        if totalDislike < 0:
                            totalDislike = 0

                        videoDetails.thumbsDown =  totalDislike

                    videoDetails.save()
                except:
                    pass

            data = {'totalLike': totalLike,'totalDislike':totalDislike, 'alreadyLiked':alreadyLiked}
            return JsonResponse(data)

            
        

def videoDisLike(request):
    if request.method == "POST":
        if request.user.is_authenticated == True:
            videoid = request.POST.get("dislikevideoID")
            user_id = request.user.id

            user = User.objects.get(id=user_id)


            #get username

            alreadyLiked = False
            alreadyDisliked = False
            
            try:
                dislikeActivity = Activity.objects.filter(user_id=user_id, video_id = videoid).exists()
                if dislikeActivity == False:
                    addDislike = Activity()
                    addDislike.thumbsUp = False
                    addDislike.thumbsDown = True
                    addDislike.user_id = user_id
                    addDislike.video_id = videoid
                    addDislike.save()
                elif dislikeActivity == True:
                    addDislike = Activity.objects.get(user_id=user_id, video_id = videoid)
                    if addDislike.thumbsUp == True and addDislike.thumbsDown == False:
                        addDislike.thumbsUp = False
                        addDislike.thumbsDown = True
                        addDislike.save()
                    else:
                        alreadyDisliked = True
            except:
                pass

            try:
                likeActivity = Activity.objects.filter(user_id=user_id, video_id = videoid).exists()
                if likeActivity == False:
                    addLike = Activity()
                    addLike.thumbsUp = True
                    addLike.thumbsDown = False
                    addLike.user_id = user_id
                    addLike.video_id = videoid
                    addLike.save()
                elif likeActivity == True:
                    addLike = Activity.objects.get(user_id=user_id, video_id = videoid)
                    if addLike.thumbsUp == False and addLike.thumbsDown == True:
                        addLike.thumbsUp = True
                        addLike.thumbsDown = False
                        addLike.save()
                    else:
                        alreadyLiked = True
            except:
                pass
            
            videoDetails = Video.objects.get(id=videoid)
            totalDisLike = videoDetails.thumbsDown
            totalLike = videoDetails.thumbsUp

            user_details = User.objects.get(id=user_id)
                
            account_details = {}

            try:
                if len(user_details.steem) >= 6:
                    account_details['steem'] = {}
                    steem_details = SteemVideo.objects.get(video_id=videoid)
                    account_details['steem']['username'] = user_details.steem_name
                    account_details['steem']['key'] = user_details.steem
                    account_details['steem']['author'] = steem_details.author
                    account_details['steem']['permlink'] = steem_details.permlink
            except:
                pass

            try:
                if len(user_details.smoke) >= 6:
                    account_details['smoke'] = {}
                    smoke_details = SmokeVideo.objects.get(video_id=videoid)
                    account_details['smoke']['username'] = user_details.smoke_name
                    account_details['smoke']['key'] = user_details.smoke
                    account_details['smoke']['author'] = smoke_details.author
                    account_details['smoke']['permlink'] = smoke_details.permlink
            except:
                pass

            
            try:
                if len(user_details.whaleshare) >= 6:
                    account_details['whaleshare'] = {}
                    whaleshare_details = WhaleShareVideo.objects.get(video_id=videoid)
                    account_details['whaleshare']['username'] = user_details.whaleshare_name
                    account_details['whaleshare']['key'] = user_details.whaleshare
                    account_details['whaleshare']['author'] = whaleshare_details.author
                    account_details['whaleshare']['permlink'] = whaleshare_details.permlink
            except:
                pass

            print(account_details)

            if alreadyDisliked == False:
                dislike_thread = Thread(target=perform_likes_dislike, args=(account_details, -1,))    
                dislike_thread.start()
                
                try:
                    totalDisLike = videoDetails.thumbsDown + len(account_details)
                    videoDetails.thumbsDown = totalDisLike

                    if alreadyLiked == True:
                        totalLike = totalLike - len(account_details)

                        if (totalLike < 0):
                            totalLike  = 0

                        videoDetails.thumbsUp =  totalLike

                    videoDetails.save()
                except:
                    pass
            
            data = {'totalDisLike': totalDisLike,'totalLike':totalLike,  'alreadyDisliked':alreadyDisliked}
            return JsonResponse(data)
        