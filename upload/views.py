import os.path
import subprocess

import random

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .forms import FileUploadModelForm

import cv2
import ipfsapi
import json
from .forms import postOptionsForm
from upload.models import Video, SteemVideo, WhaleShareVideo, SmokeVideo
from beem import Steem
from beem.comment import Comment
from register.models import User
import time
import logging
import uuid

from .models import File
from .forms import FileUploadModelForm


def get_unique_permlink(title):
    title=title.lower()
    title = title.replace(" ", "-")
    uid = uuid.uuid4()
    title = title + "-" + uid.hex[:8]
    print("The unique title is: {}".format(title))
    return title

def ajax_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            file = request.FILES['file'].read()
            current_name = ''.join(random.choice('0123456789ABCDEF') for i in range(16)) + "." + str(request.FILES['file']).split('.')[-1]
            videos_directory = os.path.join(os.path.join(settings.BASE_DIR, "static"), 'videos')


            if not(os.path.isdir(videos_directory)):
                os.makedirs(videos_directory)

            open(os.path.join(videos_directory, current_name), 'wb').write(file)
            
            # Connect to the ipfs through ipfsapi and add the uploaded file to the ipfs
            api = ipfsapi.connect('127.0.0.1', 5001)
            fileHash = api.add_bytes(file)
            

            # Define the path to save the thumbnail of the uploaded video
            path = os.path.join(os.path.join(settings.BASE_DIR, "static"), 'images') 

            thumbnail_name = '%s%s' % (''.join(random.choice('0123456789ABCDEF') for i in range(16)) +'video_Pranish', 'thumb.jpg')
            thumbnail_path = os.path.join(path, thumbnail_name)
            

            # Generate the thumnail of the video using ffmpeg tool
            runCommand = 'ffmpeg -ss 00:0:01 -i '+ os.path.join(videos_directory, current_name) +' -frames:v 1 '+ thumbnail_path
            # ffMpegPAth = "C:\\ffmpeg\\bin"
            # runCommand = ffMpegPAth + "\\" + runCommand
            subprocess.check_call(runCommand.split(" ")) #we have a command line injection vulnerability here

            durationCommand = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ' + os.path.join(videos_directory, current_name)
   
            # durationCommand = ffMpegPAth + "\\" + durationCommand
            time = ''
            duration = subprocess.check_output(durationCommand.split(' '))
            floatDuration = float(duration)/60
            decimal = floatDuration - int(floatDuration)
            seconds = int(decimal*60)
            
            if int(floatDuration) > 60:
                hours = int(floatDuration/60)
                minutes = int(floatDuration - hours*60)
                time = str(hours) + ':' + str(minutes) + ':' + str(seconds).zfill(2)
            else:
                time = str(int(floatDuration)) + ':' + str(seconds).zfill(2)


            # Find the resolution of the uploaded video
            vid = cv2.VideoCapture(os.path.join(videos_directory, current_name))
            height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            vid.release()

            hash = "{\"" + str(height) + "\": \"" + fileHash + "\", \n"

            # Declare the supported resolution 
            resolution = [2160, 1440, 1080, 720, 480, 360, 240  , 144]

            # Generate multiple video quality to upload to the server

            newHash = api.add(os.path.join(videos_directory, current_name))
            hash = hash + "\"" + str(720) + "\": \"" + newHash['Hash'] + "\"}"

            thumbnailHash = api.add(thumbnail_path)
            video = Video(views=0, duration=time, thumbsUp=0, thumbsDown=0, video=hash, user_id=request.user.id, thumbNail=thumbnailHash['Hash'])
            video.save()
            
            try:
                os.remove(thumbnail_path)
                os.remove(os.path.join(videos_directory, current_name))
            except:
                    
                print('Delete Error')

            request.session['video_id'] = video.id
            request.session['hash'] = fileHash
            
            data = []
            return JsonResponse(data, safe=False)
        else:
            data = {'error_msg': "Only jpg, pdf and xlsx files are allowed."}
            return JsonResponse(data)
    return JsonResponse({'error_msg': 'only POST method accpeted.'})


def after_clicked(request):
    return render(request, 'upload/uploading.html') 

# Create your views here.
def index(request):
    if request.user.is_authenticated == True:
        if request.method == 'POST':
            current = Video.objects.get(id=request.session.get('video_id'))
            hash = json.loads(current.video) 

            bestHash = ''

            resolution = [2160, 1440, 1080, 720, 480, 360, 240  , 144]

            for each_res in resolution:
                if str(each_res) in current.video:
                    bestHash = hash[str(each_res)]
                    break 

            optform = postOptionsForm()
            optform = postOptionsForm(request.POST)
            form = optform
            
            if form.is_valid():
                name = form.cleaned_data['name']
                steemPost = form.cleaned_data['steem']
                smokePost = form.cleaned_data['smoke']
                whalePost = form.cleaned_data['whale']

                if name != '':
                    if request.POST.getlist("#"):
                        current.name = name
                        current.nsfw = True
                    else:
                        current.name = name
                        current.nsfw = False
                else:
                    if request.POST.getlist("#"):
                        current.nsfw = True
                    else:
                        current.nsfw = False

                #current.tags = form.cleaned_data['video_tags']
                current.description =form.cleaned_data['description']
                current.language = form.cleaned_data['language']
                current.publish = True
                current.save()
                
                arb_url = 'https://vidsocial.org/watch/'+ bestHash + '/'+ str(current.id) + '/'
                thumbnail_url = 'https://gateway.ipfs.io/ipfs/' + current.thumbNail
                body = get_body(name, thumbnail_url, arb_url, current.description)
                tags = ['vidsocial']
                name = current.name
                print(name)

                if steemPost == True and request.user.steem != 'false' and request.user.steem_name != 'false':
                    try:
                        print("Steem: {} Steem Name: {}".format(request.user.steem, request.user.steem_name))
                        try:
                            s_res = post_steem(request.user.steem, request.user.steem_name, tags, name, body)
                        except Exception as e:
                            print("error in posting: {}".format(str(e)))
                            permlink=get_unique_permlink(name)
                            s_res = post_steem(request.user.steem, request.user.steem_name, [permlink], name, body)
                        
                        save_data(s_res, 'steem', current.id, tags)
                    except Exception as e:
                        print(str(e))
                        print('Errorsss')
                else:
                    print('No Steem')

                if whalePost == True and request.user.whaleshare != 'false' and request.user.whaleshare_name != 'false':
                    try:
                        print("Whale: {} Whale Name: {}".format(request.user.whaleshare, request.user.whaleshare_name))
                        
                        try:
                            wls_res = post_whaleshare(request.user.whaleshare, request.user.whaleshare_name, tags, name, body)
                        except Exception as e:
                            print("error in posting: {}".format(str(e)))
                            permlink=get_unique_permlink(name)
                            wls_res = post_whaleshare(request.user.whaleshare, request.user.whaleshare_name, [permlink], name, body)
                        
                        save_data(wls_res, 'whale', current.id, tags)
                    except Exception as e:
                        print(str(e))
                        print('Error Whale')
                else:
                    print('No Whaleshare')

                if smokePost == True and request.user.smoke != 'false' and request.user.smoke_name != 'false':
                    try:
                        print("Smoke: {} Smoke Name: {}".format(request.user.smoke, request.user.smoke_name))

                        try:
                            smk_res = post_smoke(request.user.smoke, request.user.smoke_name, tags, name, body)
                        except Exception as e:
                            print("error in posting: {}".format(str(e)))
                            permlink=get_unique_permlink(name)
                            smk_res = post_smoke(request.user.smoke, request.user.smoke_name, [permlink], name, body)


                        
                        save_data(smk_res, 'smoke', current.id, tags)
                    except Exception as e:
                        print(str(e))
                        print('Error smoke')
                else:
                    print('No smoke')

                return redirect('watch:index', video_hash=bestHash, video_id=current.id)
        
        optform = postOptionsForm()
        form = FileUploadModelForm()
        
        user = User.objects.get(id=request.user.id)
        
        key ={}
        if user.steem == 'false':
            key['steemchk'] = False
        else:
            key['steemchk'] = True

        if user.smoke == 'false':
            key['smokechk'] = False
        else:
            key['smokechk'] = True

        if user.whaleshare == 'false':
            key['whalechk'] = False
        else:
            key['whalechk'] = True

        return render(request, 'upload/upload.html', {'form': form, 'postOptionsForm': postOptionsForm, 'keychk':key})

    else:
        return redirect('/login')

def get_body(title, thumbnail, url, description):
    body = '<html><p><img src="{}" width="480" height="360"/></p> <p><a href="{}">{}</a></p><p>{}</p></html>'.format(thumbnail, url, title, description) 
    return body

def post_steem(steem_key, steem_username, tags, title, body, permlink=None):
    nodelist_one = ['https://api.steemit.com/', 'http://appbasetest.timcliff.com/']
    nodelist_two = ['http://rpc.buildteam.io', 'http://rpc.curiesteem.com/']
    nodelist_three = ['https://rpc.steemliberator.com/', 'http://rpc.steemviz.com/']
    nodelist_four = ['http://steemd.minnowsupportproject.org/', 'http://steemd.privex.io/']

    s = Steem(keys=[steem_key], nodes=nodelist_one)
    s_res = s.post(title=title, body=body, author=steem_username, tags=tags, permlink=permlink, beneficiaries=[{'account': 'fiasteem', 'weight': 2500}])
    return s_res

def post_smoke(smoke_key, smoke_username, tags, title, body, permlink=None):
    smk = Steem(node=['https://rpc.smoke.io/'], keys=[smoke_key], custom_chains={"SMOKE": {
        "chain_id": "1ce08345e61cd3bf91673a47fc507e7ed01550dab841fd9cdb0ab66ef576aaf0",
        "min_version": "0.0.0",
        "prefix": "SMK",
        "chain_assets": [
            {"asset": "STEEM", "symbol": "SMOKE", "precision": 3, "id": 1},
            {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
        ]
    }})

    smk_res = smk.post(title=title, body=body, author=smoke_username, tags=tags, permlink=permlink, json_metadata={
                        'extensions': [[0, {
                            'beneficiaries': [
                                {'account': 'fiasteem', 'weight': 2500},
                            ]}
                        ]]
                    })

    return smk_res

def post_whaleshare(whaleshares_key, whaleshares_username, tags, title, body, permlink=None):
    wls = Steem(node=["https://rpc.whaleshares.io", "ws://188.166.99.136:8090", "ws://rpc.kennybll.com:8090"], keys=[whaleshares_key])
        
    wls_res = wls.post(title=title, body=body, author=whaleshares_username, tags=tags, permlink=permlink, json_metadata={
                    'extensions': [[0, {
                        'beneficiaries': [
                            {'account': 'fiasteemproject', 'weight': 2500},
                        ]}
                    ]]
                })

    return wls_res

def save_data(data, platform, id, tags):
    permlink = data['operations'][0][1]['permlink']
    author = data['operations'][0][1]['author']
    tag = data['operations'][0][1]['parent_permlink']
    print(tag)
    
    if platform == 'smoke':
        post_url = "https://smoke.io/@{}/{}".format(author, permlink)
        print(id)
        smoke = SmokeVideo(video_id=int(id), permlink=permlink, author=author, tags=tags, post_url=post_url)
        smoke.save()

    if platform == 'whale':
        post_url = "https://whaleshares.io/{}/@{}/{}".format(tag, author, permlink)
        whale = WhaleShareVideo(video_id=int(id), permlink=permlink, author=author, tags=tags, post_url=post_url)
        whale.save()
        

    if platform == 'steem':
        post_url = "https://steemit.com/{}/@{}/{}".format(tag, author, permlink)
        steem = SteemVideo(video_id=int(id), permlink=permlink, author=author, tags=tags, post_url=post_url)
        steem.save()
        