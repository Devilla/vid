from django.shortcuts import render,redirect 
from upload.models import Video, SteemVideo, WhaleShareVideo, SmokeVideo
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

def upvote(s, author, permlink):
    acc = Comment("@{}/{}".format(author, permlink), steem_instance=s)
    votes = acc.upvote(voter=author)

def downvote(s, author, permlink):
    acc = Comment("@{}/{}".format(author, permlink), steem_instance=s)
    votes = acc.downvote(voter=author)

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


def update_payout(steem_price, smoke_price, whaleshare_price):
    '''
    Updates all payouts
    '''
    get_videos = Video.objects.all()
    total_earning = 0.0

    for all_videos in get_videos:
            try:
                single_val = SteemVideo.objects.get(video_id=all_videos.id)

                permlink = single_val.permlink
                author = single_val.author
    
                steem_payout = get_payout(s_no_auth, author, permlink) * steem_price
                total_earning = total_earning + steem_payout

                all_videos.steem = steem_payout

                print("Updated")
            except Exception as e: 
                print('No Steem. Error is {}'.format(str(e)))

            try:
                single_val = SmokeVideo.objects.get(video_id=all_videos.id)

                permlink = single_val.permlink
                author = single_val.author
    
                smoke_payout = get_payout(sm_no_auth, author, permlink) * smoke_price
                total_earning = total_earning + smoke_payout
                
                all_videos.smoke = smoke_payout

                print("Updated")
            except Exception as e: 
                print('No Smoke. Error is {}'.format(str(e)))

            try:
                single_val = SmokeVideo.objects.get(video_id=all_videos.id)

                permlink = single_val.permlink
                author = single_val.author
    
                whale_payout = get_payout(w_no_auth, author, permlink) * whaleshare_price
                total_earning = total_earning + whale_payout
                
                all_videos.whaleshares = whale_payout

                print("Updated")
            except Exception as e: 
                print('No Whaleshares. Error is {}'.format(str(e)))

            all_videos.total_earning = total_earning
            all_videos.save()

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

    latest_price = AssetPrice.objects.all().order_by('-curr_time')[:1][0]
    steem_price = latest_price.steem_price
    smoke_price = latest_price.smoke_price
    whaleshare_price = latest_price.whaleshare_price

    update_payout(steem_price, smoke_price, whaleshare_price)

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
    

    return render(request, "core/home.html", {'instance': featured, 'trend': trending, 
                                                  'subscription': channels})

def videoLike(request):
    if request.method == "POST":
        if request.user.is_authenticated == True:
            videoid = request.POST.get("likevideoID")
            user_id = request.user.id
            
            user_details = User.objects.get(id=user_id)
            try:
                steem_details = SteemVideo.objects.get(video_id=videoid)
                s = Steem(keys=[user_details.steem], nodes=["https://api.steemit.com", "https://rpc.buildteam.io"])
                upvote(s, steem_details.author, steem_details.permlink)
            except:
                pass

            try:
                whale_details = WhaleShareVideo.objects.get(video_id=videoid)
                wls = Steem(node=["https://rpc.whaleshares.io", "ws://188.166.99.136:8090", "ws://rpc.kennybll.com:8090"], keys=[user_details.whaleshare])
                upvote(wls, whale_details.author, whale_details.permlink)
            except:
                pass

            try:
                smoke_details = SmokeVideo.objects.get(video_id=videoid)

                smk = Steem(node=['https://rpc.smoke.io/'], keys=[user_details.smoke], custom_chains={"SMOKE": {
                        "chain_id": "1ce08345e61cd3bf91673a47fc507e7ed01550dab841fd9cdb0ab66ef576aaf0",
                        "min_version": "0.0.0",
                        "prefix": "SMK",
                        "chain_assets": [
                            {"asset": "STEEM", "symbol": "SMOKE", "precision": 3, "id": 1},
                            {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
                        ]
                    }})

                upvote(wls, smoke_details.author, smoke_details.permlink)
            except:
                pass
            
            totalLike = 0
            try:
                videoDetails = Video.objects.get(id=videoid)
                totalLike = videoDetails.thumbsUp + 1
                videoDetails.thumbsUp = totalLike
                videoDetails.save()
            except:
                pass
            data = {'totalLike': totalLike}
            return JsonResponse(data)

            
        

def videoDisLike(request):
    if request.method == "POST":
        if request.user.is_authenticated == True:
            videoid = request.POST.get("dislikevideoID")
            user_id = request.user.id
            
            user_details = User.objects.get(id=user_id)
            
            try:
                steem_details = SteemVideo.objects.get(video_id=videoid)
                s = Steem(keys=[user_details.steem], nodes=["https://api.steemit.com", "https://rpc.buildteam.io"])
                downvote(s, steem_details.author, steem_details.permlink)
            except:
                pass

            try:
                whale_details = WhaleShareVideo.objects.get(video_id=videoid)
                wls = Steem(node=["https://rpc.whaleshares.io", "ws://188.166.99.136:8090", "ws://rpc.kennybll.com:8090"], keys=[user_details.whaleshare])
                downvote(wls, whale_details.author, whale_details.permlink)
            except:
                pass

            try:
                smoke_details = SmokeVideo.objects.get(video_id=videoid)

                smk = Steem(node=['https://rpc.smoke.io/'], keys=[user_details.smoke], custom_chains={"SMOKE": {
                        "chain_id": "1ce08345e61cd3bf91673a47fc507e7ed01550dab841fd9cdb0ab66ef576aaf0",
                        "min_version": "0.0.0",
                        "prefix": "SMK",
                        "chain_assets": [
                            {"asset": "STEEM", "symbol": "SMOKE", "precision": 3, "id": 1},
                            {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
                        ]
                    }})

                downvote(wls, smoke_details.author, smoke_details.permlink)
            except:
                pass
            
            totalDisLike = 0
            try:
                videoDetails = Video.objects.get(id=videoid)
                totalDisLike = videoDetails.thumbsDown + 1
                videoDetails.thumbsDown = totalDisLike
                videoDetails.save()
            except:
                pass
            
            data = {'totalDisLike': totalDisLike}
            return JsonResponse(data)
        