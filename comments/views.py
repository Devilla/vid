from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import commentForm
from .models import commentsModel, CommentReplies
from upload.models import Video
# Create your views here.

def userComments(request):
    if request.user.is_authenticated == True:
        if request.method == 'POST':
            comment = request.POST.get("id_comment")
            video_id = request.POST.get("id_video")
            #commentActivity = commentsModel.objects.filter(user=request.user.id, video = video_id).exists()
            addComment = commentsModel()
            addComment.user = request.user
            addComment.video = Video.objects.get(id = video_id)
            addComment.comment = comment
            addComment.userName = str(request.user.first_name) +' '+ str(request.user.last_name)
            addComment.save()

            data = {'comment':comment, 'status':'success','userName':addComment.userName, 'uid':addComment.user.id, 'profilepic':addComment.user.profile_picture}
            return JsonResponse(data)
        else:
            data = {'status':'error'}
            return JsonResponse(data)
    else:
        return redirect('/login')

def commentReplies(request):
    if request.user.is_authenticated == True:
        if request.method == 'POST':
            comment_id = request.POST.get("comment_id")
            print(comment_id)
            
            reply = request.POST.get("reply")
            print(reply)

            #commentActivity = commentsModel.objects.filter(user=request.user.id, video = video_id).exists()
            addReply = CommentReplies()
            addReply.user = request.user
            addReply.comment = commentsModel.objects.get(id = comment_id)
            addReply.userName = str(request.user.first_name) +' '+ str(request.user.last_name)
            addReply.reply = reply
            addReply.save()

            data = {'comment':reply, 'userName': addReply.userName, 'profilepic':addReply.user.profile_picture, 'uid': addReply.user.id, 'cmnt_id':comment_id, 'status':'success'}
            return JsonResponse(data)
        else:
            data = {'status':'error'}
            return JsonResponse(data)
    else:
        return redirect('/login')