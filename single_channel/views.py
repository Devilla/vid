from django.shortcuts import render
from upload.models import Video
from register.models import User
import json
import demjson
# Create your views here.

def DetailView(request, pk):
        video = Video.objects.filter(user_id=pk)

        resolution = [2160, 1440, 1080, 720, 480, 360, 240  , 144]

        for each_videot in video:
                for each_res in resolution:
                        if str(each_res) in each_videot.video:
                                hasht = demjson.decode(each_videot.video)
                                each_videot.bestHash_Trending = hasht[str(each_res)]
                                break  

        ch = User.objects.get(id=pk)
        print(ch)
        return render(request, 'single_channel/detail.html', {'video': video, 'channel':ch.channel_name })  
