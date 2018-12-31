from django.shortcuts import render,redirect 
from upload.models import Video, SteemVideo, WhaleShareVideo, SmokeVideo
from register.models import User
from django.http import JsonResponse
from django.http import HttpResponse
from .forms import videoLikeForm, videoDisLikeForm
import json
import demjson
from core.models import AssetPrice
from datetime import datetime
import pytz
import requests
import json

def get_payout(s, author, permline):
    try:
        acc = Comment("@{}/{}".format(author, permlink), steem_instance=s)
        payout = float(str(acc.reward).split()[0])
    except:
        payout = 0.00
    
    return payout

# Create your views here.
def index(request):
    if (len(AssetPrice.objects.all())) == 0:
        AssetPrice().save()

    latest_price = AssetPrice.objects.all().order_by('-curr_time')[:1][0]
    steem_price = latest_price.steem_price
    smoke_price = latest_price.smoke_price
    whaleshare_price = latest_price.whaleshare_price
    latest_date = latest_price.curr_time
    substract = datetime.utcnow().replace(tzinfo=pytz.UTC) - latest_date

    if int(substract.seconds/60) >= 180:
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
            permlink = steem[0].permlink
            author = steem[0].author
            #update the earning every hour too
        except: 
            print('No Steem')

        try:
            smoke = SmokeVideo.objects.filter(video_id=each_video.id)
        except: 
            print('No Smoke')

        try:
            whale = WhaleShareVideo.objects.filter(video_id=each_video.id)
        except: 
            print('No Whaleshare')

        for each_res in resolution:
            if str(each_res) in each_video.video:
                hash = demjson.decode(each_video.video)
                each_video.bestHash_Featured = hash[str(each_res)]
                break   

    for each_videot in trending:
        
        pay = 0
        # try:
        #     steem = SteemVideo.objects.filter(video_id=each_videot.id)
        #     steem_pay = SteemManager.get_payout(steem.post)
        #     pay = pay + steem_pay
        # except: 
        #     print('No Steem')

        # try:
        #     whale = WhaleShareVideo.objects.filter(video_id=each_videot.id)
        #     whale_pay = WhalesharesManger.get_payout(whale.post)
        #     pay = pay + whale_pay
        # except: 
        #     print('No Whale')

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
            channels.remove(each_channel)
            # each_channel.count = 0
    
    likeform = videoLikeForm()
    dislikeform = videoDisLikeForm()
    return render(request, "core/home.html", {'instance': featured, 'trend': trending, 
                                                  'subscription': channels, 'likeform':likeform, 'dislikeform':dislikeform})

def videoLike(request):
    if request.method == "POST":
        if request.user.is_authenticated == True:
            form = videoLikeForm(request.POST)
            if form.is_valid():
                videoid = form.cleaned_data.get("likevideoID")
                print("video id")
                print(videoid)

                
            user_id = request.user.id
            print ("user id")
            print(user_id)
            


            return redirect('/')