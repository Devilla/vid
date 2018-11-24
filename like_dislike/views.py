from django.shortcuts import render, HttpResponse
from upload.models import Video
from like_dislike.models import Activity
from register.models import User

# Create your views here.
def like(request):
    
    if request.method == 'GET':
        video_id = request.GET['video_id']
        video = Video.objects.get(id=video_id)

        

        try :
            activity = Activity.objects.get(user_id=request.user.id, video_id=video.id)

            if activity.thumbsUp == True:
                likes =[video.thumbsUp, video.thumbsDown]
                return HttpResponse(likes)
                
            else:
                dislikes = video.thumbsDown - 1
                video.thumbsDown = dislikes
                likes = video.thumbsUp + 1
                video.thumbsUp = likes
                video.save()
                activity.thumbsUp = True
                activity.thumbsDown = False
                activity.save()
                like = [likes, dislikes]
                return HttpResponse(like)
        except:
            likes = video.thumbsUp + 1
            video.thumbsUp = likes
            activity = Activity(user_id=request.user.id, video_id=video.id, thumbsUp=True, thumbsDown=False)
            video.save()
            activity.save()
            like = [likes, video.thumbsDown]
            return HttpResponse(like)


def dislike(request):
    
    if request.method == 'GET':
        video_id = request.GET['video_id']
        video = Video.objects.get(id=video_id)


        try :
            activity = Activity.objects.get(user_id=request.user.id, video_id=video.id)

            if activity.thumbsUp == True:
                likes = video.thumbsUp - 1
                video.thumbsUp = likes
                dislikes = video.thumbsDown + 1
                video.thumbsDown = dislikes
                video.save()
                activity.thumbsUp = False
                activity.thumbsDown = True
                activity.save()
                like = [likes, dislikes]
                return HttpResponse(like)

            else:
                like = [video.thumbsUp, video.thumbsDown]
                return HttpResponse(like)
        except:
            dislikes = video.thumbsDown + 1
            video.thumbsDown = likes
            activity = Activity(user_id=request.user.id, video_id=video.id, thumbsUp=False, thumbsDown=True)
            video.save()
            activity.save()
            like = [video.thumbsUp, dislikes]
            return HttpResponse(like)