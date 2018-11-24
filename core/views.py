from django.shortcuts import render
from upload.models import Video
import json
import demjson

# Create your views here.
def index(request):
    
    featured = Video.objects.all().order_by('-id')[:8]
    trending = Video.objects.all().order_by('-views')[:8]
    channels = Video.objects.all().order_by('-id')[:11]

    bestHash_Featured = []
    bestHash_Trending = []

    resolution = [2160, 1440, 1080, 720, 480, 360, 240  , 144]

    for each_video in featured:
        for each_res in resolution:
            if str(each_res) in each_video.video:
                hash = demjson.decode(each_video.video)
                each_video.bestHash_Featured = hash[str(each_res)]
                bestHash_Featured.append(hash[str(each_res)])
                break   

    for each_video in trending:
        for each_res in resolution:
            if str(each_res) in each_video.video:
                hash = demjson.decode(each_video.video)
                each_video.bestHash_Trending = hash[str(each_res)]
                bestHash_Trending.append(hash[str(each_res)])
                break   

    return render(request, "core/home.html", {'instance': featured, 'trend': trending, 
                                                  'subscription': channels })
