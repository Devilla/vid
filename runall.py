import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ipfs.settings")

django.setup()

from core.models import AssetPrice
from upload.models import Video, SteemVideo, WhaleShareVideo, SmokeVideo, TrendingVideo, HotVideo
from register.models import User
from single_channel.models import followersModel
from beem import Steem
from beem.comment import Comment
from beem.account import Account
import ipfsapi
import psutil
import time
import subprocess
from urllib.request import urlopen
import os
from django_pandas.io import read_frame
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import json
from comments.models import CustomThreadedComment, commentLDinfo
from steem import Steem as SteemOriginal
import threading

try:
    s_no_auth = Steem(nodes=["http://seed1.blockbrothers.io:2001", "http://seed.liondani.com:2016", "https://api.steemit.com", "https://rpc.buildteam.io"])
except:
    pass

try:
    w_no_auth = Steem(node=["https://wls.kennybll.com", "wss://wls.kennybll.com", "ws://rpc.kennybll.com:8090", "https://rpc.whaleshares.io", "ws://188.166.99.136:8090"])
except:
    pass

try:
    sm_no_auth = Steem(node=['https://rpc.smoke.io/'], custom_chains={"SMOKE": {
                    "chain_id": "1ce08345e61cd3bf91673a47fc507e7ed01550dab841fd9cdb0ab66ef576aaf0",
                    "min_version": "0.0.0",
                    "prefix": "SMK",
                    "chain_assets": [
                        {"asset": "STEEM", "symbol": "SMOKE", "precision": 3, "id": 1},
                        {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
                    ]
                }})
except:
    pass

def upvote(s, permlink, voter):
    acc = Comment(permlink, steem_instance=s)
    votes = acc.upvote(voter=voter)

def downvote(s, permlink, voter):
    acc = Comment(permlink, steem_instance=s)
    votes = acc.downvote(voter=voter)

def like_comments():
    for likeinfo in commentLDinfo.objects.all():
        if likeinfo.LDcomment.steem_id != "" and likeinfo.steem_like == False:
            s = Steem(nodes=["http://seed1.blockbrothers.io:2001", "http://seed.liondani.com:2016", "https://api.steemit.com", "https://rpc.buildteam.io"], keys=[likeinfo.LDuser.steem])
            
            if likeinfo.like == True and likeinfo.steem_like == False:
                try:
                    upvote(s, likeinfo.LDcomment.steem_id, likeinfo.LDuser.steem_name)
                    likeinfo.steem_like = True
                    likeinfo.steem_dislike = False
                    likeinfo.save()
                    
                except Exception as e:
                    print("Error liking: {}".format(str(e)))
            elif likeinfo.dislike == True and likeinfo.steem_dislike == False:
                try:
                    downvote(s, likeinfo.LDcomment.steem_id, likeinfo.LDuser.steem_name)
                    likeinfo.steem_dislike = True
                    likeinfo.steem_like = False
                    likeinfo.save()
                    
                except Exception as e:
                    print("Error disliking: {}".format(str(e)))
                    
        if likeinfo.LDcomment.smoke_id != "" and likeinfo.smoke_like == False:
            s = Steem(node=['https://rpc.smoke.io/'], keys=[likeinfo.LDuser.smoke], custom_chains={"SMOKE": {
                            "chain_id": "1ce08345e61cd3bf91673a47fc507e7ed01550dab841fd9cdb0ab66ef576aaf0",
                            "min_version": "0.0.0",
                            "prefix": "SMK",
                            "chain_assets": [
                                {"asset": "STEEM", "symbol": "SMOKE", "precision": 3, "id": 1},
                                {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
                            ]
                        }})
            
            if likeinfo.like == True and likeinfo.smoke_like == False:
                try:
                    upvote(s, likeinfo.LDcomment.smoke_id, likeinfo.LDuser.smoke_name)
                    likeinfo.smoke_like = True
                    likeinfo.smoke_dislike = False
                    likeinfo.save()
                    
                except Exception as e:
                    print("Error liking: {}".format(str(e)))
            elif likeinfo.dislike == True and likeinfo.smoke_dislike == False:
                try:
                    downvote(s, likeinfo.LDcomment.smoke_id, likeinfo.LDuser.smoke_name)
                    likeinfo.smoke_dislike = True
                    likeinfo.smoke_like = False
                    likeinfo.save()
                    
                except Exception as e:
                    print("Error disliking: {}".format(str(e)))
                    
        if likeinfo.LDcomment.whaleshare_id != "" and likeinfo.whaleshare_like == False:
            s = Steem(node=["https://wls.kennybll.com", "https://rpc.whaleshares.io", "ws://188.166.99.136:8090"], keys=[likeinfo.LDuser.whaleshare])
            
            if likeinfo.like == True and likeinfo.whaleshare_like == False:
                try:
                    upvote(s, likeinfo.LDcomment.whaleshare_id, likeinfo.LDuser.whaleshare_name)
                    likeinfo.whaleshare_like = True
                    likeinfo.whaleshare_dislike = False
                    likeinfo.save()
                    
                except Exception as e:
                    print("Error liking: {}".format(str(e)))
            elif likeinfo.dislike == True and likeinfo.whaleshare_dislike == False:
                try:
                    downvote(s, likeinfo.LDcomment.whaleshare_id, likeinfo.LDuser.whaleshare_name)
                    likeinfo.whaleshare_dislike = True
                    likeinfo.whaleshare_like = False
                    likeinfo.save()
                    
                except Exception as e:
                    print("Error disliking: {}".format(str(e)))

def push_comments():
    for comment in CustomThreadedComment.objects.all():
        reply = comment.comment
        
        if comment.steem_id == "" and comment.user.steem != "":
            try:
                steem_username = comment.user.steem_name
                steem_key = comment.user.steem

                if comment.parent_id == None:
                    st_obj = SteemVideo.objects.get(video_id=comment.content_object.id)
                    parent = "@{}/{}".format(st_obj.author, st_obj.permlink)
                else:
                    cs_object = CustomThreadedComment.objects.get(id=comment.parent_id)
                    parent = cs_object.steem_id
                
                if len(parent) > 3:
                    
                    if comment.steem_id == "":
                        s = SteemOriginal(keys=[steem_key])
                        data = s.commit.post(title="", body=reply, reply_identifier=parent, author=steem_username)
                        comment.steem_id = "@{}/{}".format(data['operations'][0][1]['author'], data['operations'][0][1]['permlink'])
                        comment.save()
            except Exception as e:
                print("Error in steem: {}".format(str(e)))
                
        if comment.smoke_id == "" and comment.user.smoke != "":
            try:
                smoke_username = comment.user.smoke_name
                smoke_key = comment.user.smoke

                if comment.parent_id == None:
                    st_obj = SmokeVideo.objects.get(video_id=comment.content_object.id)
                    parent = "@{}/{}".format(st_obj.author, st_obj.permlink)
                else:
                    cs_object = CustomThreadedComment.objects.get(id=comment.parent_id)
                    parent = cs_object.smoke_id
                
                if len(parent) > 3:
                    if comment.smoke_id == "":
                        s = Steem(node=['https://rpc.smoke.io/'], keys=[smoke_key], custom_chains={"SMOKE": {
                            "chain_id": "1ce08345e61cd3bf91673a47fc507e7ed01550dab841fd9cdb0ab66ef576aaf0",
                            "min_version": "0.0.0",
                            "prefix": "SMK",
                            "chain_assets": [
                                {"asset": "STEEM", "symbol": "SMOKE", "precision": 3, "id": 1},
                                {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
                            ]
                        }})

                        data = s.post(title="", body=reply, reply_identifier=parent, author=smoke_username)
                        comment.smoke_id = "@{}/{}".format(data['operations'][0][1]['author'], data['operations'][0][1]['permlink'])
                        comment.save()
            except Exception as e:
                print("Error in smoke: {}".format(str(e)))
            
        if comment.whaleshare_id == "" and comment.user.whaleshare != "":
            try:
                whaleshare_username = comment.user.whaleshare_name
                whaleshare_key = comment.user.whaleshare

                if comment.parent_id == None:
                    st_obj = WhaleShareVideo.objects.get(video_id=comment.content_object.id)
                    parent = "@{}/{}".format(st_obj.author, st_obj.permlink)
                else:
                    cs_object = CustomThreadedComment.objects.get(id=comment.parent_id)
                    parent = cs_object.whaleshare_id
                
                if len(parent) > 3:
                    if comment.whaleshare_id == "":
                        s = Steem(node=["https://wls.kennybll.com", "https://rpc.whaleshares.io", "ws://188.166.99.136:8090"], keys=[whaleshare_key])

                        data = s.post(title="", body=reply, reply_identifier=parent, author=whaleshare_username)
                        comment.whaleshare_id = "@{}/{}".format(data['operations'][0][1]['author'], data['operations'][0][1]['permlink'])
                        comment.save()
            except Exception as e:
                print("Error in whaleshare: {}".format(str(e)))
    
    like_comments()

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

def get_payout(s, author, permlink):
    try:
        acc = Comment("@{}/{}".format(author, permlink), steem_instance=s)
        payout = float(str(acc.reward).split()[0])
    except Exception as e:
        print("Error in payout: {}".format(str(e)))
        payout = 0.00
    
    return payout

def update_prices():
    '''
    Gets the price for steem, smoke and whaleshares
    '''
    steem_price = 0
    smoke_price = 0
    whaleshare_price = 0

    latest_price = AssetPrice.objects.all().order_by('-curr_time')[:1][0]
    steem_price = latest_price.steem_price
    smoke_price = latest_price.smoke_price
    whaleshare_price = latest_price.whaleshare_price
    print(steem_price, smoke_price, whaleshare_price)

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
        r=requests.get("https://cryptofresh.com/api/asset/markets?asset=RUDEX.WLS")
        res = json.loads(r.text)
        p = float(res['USD']['price'])

        if p > 0:
            whaleshare_price = p
    except:
        pass
    
    AssetPrice.objects.all().delete()
    
    print("Updating price to {} {} {}".format(steem_price, smoke_price, whaleshare_price))
    a = AssetPrice(steem_price=steem_price, smoke_price=smoke_price, whaleshare_price=whaleshare_price)
    a.save()

def update_single_earning_like_dislike_followers(video_id):

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
            update_followers = followersModel.objects.all()
            
            for follower in update_followers:
                a = Account(author, steem_instance=s_no_auth)
                new_followers=a.get_follow_count()['follower_count']
                print("New followers for: {} is {}".format(author, new_followers))
                follower.total_followers = new_followers
                follower.save()
                print("Followers updated")
        except Exception as e:
            print("error updating followers: {}".format(str(e)))

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
            update_followers = followersModel.objects.all()

            for follower in update_followers:
                a = Account(author, steem_instance=sm_no_auth)
                new_followers=int(follower.total_followers) + int(a.get_follow_count()['follower_count'])
                print("New followers for: {} is {}".format(author, new_followers))
                follower.total_followers = new_followers
                follower.save()
                print("Followers updated")
        except Exception as e:
            print("error updating followers: {}".format(str(e)))

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
            update_followers = followersModel.objects.all()

            for follower in update_followers:
                a = Account(author, steem_instance=w_no_auth)
                new_followers=int(follower.total_followers) + int(a.get_follow_count()['follower_count'])
                print("New followers for: {} is {}".format(author, new_followers))
                follower.total_followers = new_followers
                follower.save()
                print("Followers updated")
        except Exception as e:
            print("error updating followers: {}".format(str(e)))

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
    
def ipfs_check():
    try:
        api = ipfsapi.connect('127.0.0.1', 5001)
    except:
        for proc in psutil.process_iter():
            if proc.name() == "ipfs":
                proc.kill()

    subprocess.Popen(["ipfs","daemon"])

def update_old_views():
    get_videos = Video.objects.all()

    for video in get_videos:
        time_difference = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()) - int(video.old_views_time.strftime("%s"))

        if time_difference >= (24 * 60 * 60):
            video.old_views = video.views
            video.old_views_time = django.utils.timezone.now()
            video.save()

def update_hot_trending():
    update_old_views()
    all_vids = Video.objects.all()

    df = read_frame(all_vids).reset_index(drop=True)

    trending = df.sort_values('views', ascending=False)

    df['hot'] = (df['views'] - df['old_views'])/df['old_views']
    df['hot'] = df['hot'].fillna(value=0)
    hot = df.sort_values('hot', ascending=False)
    
    TrendingVideo.objects.all().delete()
    HotVideo.objects.all().delete()
    
    for idx, row in hot.iterrows():
        hv = HotVideo(video=Video.objects.get(id=row['id']), rank=idx+1)
        hv.save()

    for idx, row in trending.iterrows():
        tv = TrendingVideo(video=Video.objects.get(id=row['id']), rank=idx+1)
        tv.save()  

subprocess.Popen(["python3.5","manage.py", "runserver"])
time.sleep(5)

t1 = threading.Thread(target=push_comments, args=[])

while True:
    if not t1.isAlive():
        try:
            t1.start()
        except:
            pass

    ipfs_check()
    update_hot_trending()
    get_videos = Video.objects.all()

    for all_videos in get_videos:
        video_id = all_videos.id
        update_single_earning_like_dislike_followers(video_id)
        
    time.sleep(1)