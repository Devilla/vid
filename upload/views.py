
import os.path
import subprocess

import random

from django.conf import settings
from django.shortcuts import render, redirect

import cv2
import ipfsapi
import json

from upload.models import Video



# Create your views here.
def index(request):
    if request.user.is_authenticated == True:
        if request.method == 'POST':
            try:

                # Get the uploaded file and rename it to make it unique and save locally
                file = request.FILES['video'].read()
                current_name = ''.join(random.choice('0123456789ABCDEF') for i in range(16)) + str(request.FILES['video']) 
                
                path1 = os.path.join(os.path.join(settings.BASE_DIR, "static"), 'videos')
                open(os.path.join(path1, current_name), 'wb').write(file)
                
                # Connect to the ipfs through ipfsapi and add the uploaded file to the ipfs
                api = ipfsapi.connect('127.0.0.1', 5001)
                fileHash = api.add_bytes(file)
                

                # Define the path to save the thumbnail of the uploaded video
                path = os.path.join(os.path.join(settings.BASE_DIR, "static"), 'images')                              
                thumbnail_name = '%s%s' % (''.join(random.choice('0123456789ABCDEF') for i in range(16)) +'video_Pranish', 'thumb.jpg')
                thumbnail_path = os.path.join(path, thumbnail_name)
                

                # Generate the thumnail of the video using ffmpeg tool
                runCommand = 'ffmpeg -ss 00:0:01 -i "'+ os.path.join(path1, current_name) +'" -frames:v 1 "'+ thumbnail_path + '"'
                ffMpegPAth = "C:\\ffmpeg\\bin"
                runCommand = ffMpegPAth + "\\" + runCommand
                subprocess.call(runCommand)


                # Get the duration of the video file
                durationCommand = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "' + os.path.join(path1, current_name) + '"'
                durationCommand = ffMpegPAth + "\\" + durationCommand
                time = ''
                duration = subprocess.check_output(durationCommand)
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
                vid = cv2.VideoCapture(os.path.join(path1, current_name))
                height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
                width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
                vid.release()

                hash = "{\"" + str(height) + "\": \"" + fileHash + "\", \n"

                # Declare the supported resolution 
                resolution = [2160, 1440, 1080, 720, 480, 360, 240  , 144]

                # Generate multiple video quality to upload to the server

                for small_res in resolution:
                    if small_res < height :
                        # Change the video to different quality
                        res = 'ffmpeg -v -8 -i "' + os.path.join(path1, current_name) + '" -vf scale=-2:' + str(small_res) + ' -preset slow -c:v libx264 -strict experimental -c:a aac -crf 24 -maxrate 500k -bufsize 500k -r 25 -f mp4 "' + os.path.join(path1, str(small_res)+current_name)
                        subprocess.check_call(res)
                        newHash = api.add(os.path.join(path1, str(small_res)+current_name), trickle=True)
                        os.remove(os.path.join(path1, str(small_res)+current_name))
                        
                        if small_res == 144:
                            hash = hash + "\"" + str(small_res) + "\": \"" + newHash['Hash'] + "\"}"
                        else:
                            hash = hash + "\"" + str(small_res) + "\": \"" + newHash['Hash'] + "\", \n"
                                        

                # Save the generated data in the server
                thumbnailHash = api.add(thumbnail_path)
                video = Video(views=0, duration=time, thumbsUp=0, thumbsDown=0, video=hash, user_id=request.user.id, thumbNail=thumbnailHash['Hash'])
                video.save()
                
                try:
                    os.remove(thumbnail_path)
                    os.remove(os.path.join(path1, current_name))
                except:
                    print('Delete Error')

                request.session['video_id'] = video.id
                request.session['hash'] = fileHash
                return redirect('upload:info')

            except:
                print('Not uploaded, server error')
            
                
        return render(request, 'upload/upload.html')

    else:
        return redirect('/login')

def info(request):
    if request.user.is_authenticated == True:
        current = Video.objects.get(id=request.session.get('video_id'))
        
        hash = json.loads(current.video) 

        bestHash = ''

        resolution = [2160, 1440, 1080, 720, 480, 360, 240  , 144]

        for each_res in resolution:
            if str(each_res) in current.video:
                bestHash = hash[str(each_res)]
                break 

        
        if current.user_id == request.user.id:
            
            if request.method == 'POST':
                name = request.POST.get("name")
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
                current.publish = True
                current.save()



                return redirect('watch:index', video_hash=bestHash, video_id=current.id)

            return render(request, 'upload/upload_process.html', {'filehash':request.session.get('hash')})  
        else:
            print('Not sufficient privilege')

    else:
        return redirect('/login')