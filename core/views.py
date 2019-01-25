from django.shortcuts import render,redirect 
from upload.models import Video, SteemVideo, WhaleShareVideo, SmokeVideo, TrendingVideo, HotVideo
from like_dislike.models import Activity
from register.models import User
from django.http import JsonResponse
from django.http import HttpResponse
from threading import Thread
from single_channel.models import followersModel
from beem.account import Account

import json
import demjson
from core.models import AssetPrice
import pytz
import requests
import json
from django.core import serializers
from beem import Steem
from beem.comment import Comment

def upvote(s, post_author, permlink, voter):
    acc = Comment("@{}/{}".format(post_author, permlink), steem_instance=s)
    votes = acc.upvote(voter=voter)

def downvote(s, post_author, permlink, voter):
    acc = Comment("@{}/{}".format(post_author, permlink), steem_instance=s)
    votes = acc.downvote(voter=voter)

# Create your views here
def index(request):
    if 'display_nsfw' not in request.session:
        request.session['display_nsfw'] = False

    if (len(AssetPrice.objects.all())) == 0:
        AssetPrice().save()

    trendingvideos = []
    hotvideos = []

    if request.session['display_nsfw'] == False:
        featured = Video.objects.filter(nsfw=False).order_by('-id')[:50]
    else:
        featured = Video.objects.all().order_by('-id')[:50]

    for tv in TrendingVideo.objects.all().order_by('-rank'):

        if request.session['display_nsfw'] == False:
            if tv.video.nsfw == False:
                trendingvideos.append(tv.video)
            else:
                trendingvideos.append(tv.video)
    
    for hv in HotVideo.objects.all().order_by('-rank'):

        if request.session['display_nsfw'] == False:
            if hv.video.nsfw == False:
                hotvideos.append(hv.video)
            else:
                hotvideos.append(hv.video)

    trendingJSONdata = serializers.serialize('json', trendingvideos)
    hotJSONdata = serializers.serialize('json', hotvideos)
    channels = User.objects.all().order_by('-id')[:11] 

    print(channels)

    featuredJSONdata = serializers.serialize('json', featured)

    return render(request, "core/home.html", {'instance': featured, 'trendingJSONdata':trendingJSONdata, 'hotJSONdata': hotJSONdata,'featuredJSONdata':featuredJSONdata, 'subscription': channels})

def perform_follow_unfollow(account_details):
    print("Follow unfollow function called")
    print(account_details)
    for key in account_details:
        print(key)
        try:
            if 'key' in account_details[key]:
                if key == 'steem':
                    s = Steem(keys=[account_details[key]['key']], nodes=["http://seed1.blockbrothers.io:2001", "http://seed.liondani.com:2016", "https://api.steemit.com", "https://rpc.buildteam.io"])
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
                    s = Steem(keys=[account_details[key]['key']], node=["ws://rpc.kennybll.com:8090","https://rpc.whaleshares.io", "ws://188.166.99.136:8090"])


                print(account_details[key])
                a = Account(account=account_details[key]['username'], steem_instance=s)
                a.follow(account_details[key]['author'])
        except Exception as e:
            print("Error while follow/unfollow: {}".format(str(e)))



def perform_likes_dislike(account_details, type=1):
    '''
    type(int):
    1 to like, other for dislike
    '''
    print("Like dislike function called")
    for key in account_details:
        print(key)
        try:
            if 'key' in account_details[key]:
                if key == 'steem':
                    s = Steem(keys=[account_details[key]['key']], nodes=["http://seed1.blockbrothers.io:2001", "http://seed.liondani.com:2016", "https://api.steemit.com", "https://rpc.buildteam.io"])
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
                    s = Steem(keys=[account_details[key]['key']], node=["https://wls.kennybll.com", "ws://rpc.kennybll.com:8090", "https://rpc.whaleshares.io", "ws://188.166.99.136:8090"])

                if type==1:
                    upvote(s, account_details[key]['author'], account_details[key]['permlink'], account_details[key]['username'])
                else:
                    downvote(s, account_details[key]['author'], account_details[key]['permlink'], account_details[key]['username'])
        except Exception as e:
            print("Error while like/dislike: {}".format(str(e)))

def nsfw_status(request):
    if request.method == "POST":
        nsfw_stat = request.POST.get("stat")
        if 'display_nsfw' not in request.session:
            request.session['display_nsfw'] = False
        elif nsfw_stat == "True":
            request.session['display_nsfw'] = True
        elif nsfw_stat == "False":
            request.session['display_nsfw'] = False
            
        data = {'nsfw_status': request.session['display_nsfw']}
        return JsonResponse(data)

def videoLike(request):
    if request.method == "POST":
        if request.user.is_authenticated == True:
            videoid = request.POST.get("likevideoID")
            user_id = request.user.id
            user_details = User.objects.get(id=user_id)

            alreadyLiked = False
            alreadyDisliked = False

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
                        alreadyDisliked=True
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
                    account_details['steem']['username'] = user_details.steem_name
                    account_details['steem']['permlink'] = steem_details.permlink
            except:
                pass

            try:
                if len(user_details.smoke) >=6:
                    account_details['smoke'] = {}
                    smoke_details = SmokeVideo.objects.get(video_id=videoid)
                    account_details['smoke']['key'] = user_details.smoke
                    account_details['smoke']['author'] = smoke_details.author
                    account_details['smoke']['username'] = user_details.smoke_name
                    account_details['smoke']['permlink'] = smoke_details.permlink
            except:
                pass

            try:
                if len(user_details.whaleshare) >=6:
                    account_details['whaleshare'] = {}
                    whaleshare_details = WhaleShareVideo.objects.get(video_id=videoid)
                    account_details['whaleshare']['key'] = user_details.whaleshare
                    account_details['whaleshare']['author'] = whaleshare_details.author
                    account_details['whaleshare']['username'] = user_details.whaleshare_name
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
                        alreadyLiked = True
                        addDislike.thumbsUp = False
                        addDislike.thumbsDown = True
                        addDislike.save()
                    else:
                        alreadyDisliked = True
            except:
                pass
            
            videoDetails = Video.objects.get(id=videoid)
            totalDisLike = videoDetails.thumbsDown
            totalLike = videoDetails.thumbsUp

            user_details = User.objects.get(id=user_id)
                
            account_details = {}

            try:
                if len(user_details.steem) >=6:
                    account_details['steem'] = {}
                    steem_details = SteemVideo.objects.get(video_id=videoid)
                    account_details['steem']['key'] = user_details.steem
                    account_details['steem']['author'] = steem_details.author
                    account_details['steem']['username'] = user_details.steem_name
                    account_details['steem']['permlink'] = steem_details.permlink
            except:
                pass

            try:
                if len(user_details.smoke) >=6:
                    account_details['smoke'] = {}
                    smoke_details = SmokeVideo.objects.get(video_id=videoid)
                    account_details['smoke']['key'] = user_details.smoke
                    account_details['smoke']['author'] = smoke_details.author
                    account_details['smoke']['username'] = user_details.smoke_name
                    account_details['smoke']['permlink'] = smoke_details.permlink
            except:
                pass

            try:
                if len(user_details.whaleshare) >=6:
                    account_details['whaleshare'] = {}
                    whaleshare_details = WhaleShareVideo.objects.get(video_id=videoid)
                    account_details['whaleshare']['key'] = user_details.whaleshare
                    account_details['whaleshare']['author'] = whaleshare_details.author
                    account_details['whaleshare']['username'] = user_details.whaleshare_name
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
        
def about(request):
    if request.method == 'GET':
        return render(request, 'core/about.html')

def help(request):
    if request.method == 'GET':
        return render(request, 'core/help.html')


def followChannel(request):
    if request.method == "POST":
        if request.user.is_authenticated == True:
                followingID = request.POST.get("followUnfollowID")
                checkFollowing = followersModel.objects.filter(user=request.user.id, following = followingID).exists()

                followers_details = User.objects.get(id=request.user.id)
                following_details = User.objects.get(id=followingID)


                account_details = {}

                try:
                    if len(followers_details.steem) >=6 and len(following_details.steem) >=6:
                        account_details['steem'] = {}
                        account_details['steem']['key'] = followers_details.steem
                        account_details['steem']['author'] = following_details.author
                        account_details['steem']['username'] = followers_details.steem_name
                except:
                    pass

                try:
                    if len(followers_details.smoke) >=6 and len(following_details.smoke) >=6:
                        account_details['smoke'] = {}
                        account_details['smoke']['key'] = followers_details.smoke
                        account_details['smoke']['author'] = following_details.author
                        account_details['smoke']['username'] = followers_details.smoke_name
                except:
                    pass

                try:
                    if len(followers_details.whaleshare) >=6 and len(following_details.whaleshare) >=6:
                        account_details['whaleshare'] = {}
                        account_details['whaleshare']['key'] = followers_details.whaleshare
                        account_details['whaleshare']['author'] = following_details.author
                        account_details['whaleshare']['username'] = followers_details.whaleshare_name
                except:
                    pass


                follow_unfollow_thread = Thread(target=perform_follow_unfollow, args=(account_details,))    
                follow_unfollow_thread.start()

                if checkFollowing == False:
                        addFollow = followersModel()
                        addFollow.user = request.user
                        addFollow.following = User.objects.get(id=followingID)
                        countFollowing = addFollow.total_followers + len(account_details)
                        addFollow.total_followers = countFollowing
                        addFollow.save()
                        data = {'response': 'Successfully Followed', 'status':'1', 'totalFollower':countFollowing}
                        return JsonResponse(data)
                elif checkFollowing == True:
                        removeFollow = followersModel()
                        removeFollow.objects.filter(user=request.user.id, following = followingID).delete()
                        countFollowing = addFollow.total_followers - len(account_details)

                        if countFollowing < 0:
                            countFollowing = 0
                            
                        removeFollow.total_followers = countFollowing
                        removeFollow.save()
                        
                        data = {'response': 'Successfully Unfollowed', 'status':'0','totalFollower':countFollowing, 'totalFollower':countFollowing}
                        return JsonResponse(data)
        else:
                return redirect('/login')


def singleTagVideos(request,tag):
    if request.method == "GET":
        tgvid = []
        taggedVideos = Video.objects.all()
        for video in taggedVideos:
            if video.tags!=None:
                for singletag in video.tags:
                    if singletag == tag:
                        tgvid.append(video)

        return render(request, 'core/tagVideos.html',{'taggedVideos':tgvid, 'tag':tag})
