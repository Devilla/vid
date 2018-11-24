from django.shortcuts import render, HttpResponse
from upload.models import Video
import demjson

import json
# Create your views here.


def index(request, video_hash, video_id):
    current = Video.objects.get(id=video_id)

    featured = Video.objects.all().order_by('-id')[:1]
    recommend = Video.objects.all().order_by('-views')[:1]

    resolution = [2160, 1440, 1080, 720, 480, 360, 240  , 144]



    bestHash_Featured = []
    bestHash_Recomended = []

    for each_video in featured:
        for each_res in resolution:
            if str(each_res) in each_video.video:
                hash = demjson.decode(each_video.video)
                bestHash_Featured.append(hash[str(each_res)])
                break   

    for each_video in recommend:
        for each_res in resolution:
            if str(each_res) in each_video.video:
                hash = demjson.decode(each_video.video)
                bestHash_Recomended.append(hash[str(each_res)])
                break   



    hash = json.loads(current.video)
    
    dump = json.dumps(hash)
    
    video_content = ''

    for quality, this_hash in hash.items():
        video_content = video_content + '{\n\t src: \'https://gateway.ipfs.io/ipfs/' + this_hash + '\',\n\t type: \'video/mp4\',\n\t size: ' + quality + ',\n},\n' 
    
    
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
        return render(request, "watch/base.html", {'video_hash': hash, 'view': current.views, 'dump': dump, 'cont': video_content,
                'video_id': video_id, 'thumbsUp': current.thumbsUp, 'thumbsDown': current.thumbsDown, 'name': current.name,
                'latest' : featured, 'recommended': recommend, 
                'bestHash_Featured': bestHash_Featured,'bestHash_Recomended': bestHash_Recomended })
    
