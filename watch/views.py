from django.shortcuts import render, HttpResponse
from upload.models import Video, SteemVideo, WhaleShareVideo, SmokeVideo
from comments.forms import commentForm
from register.models import User
import demjson
from like_dislike.models import Activity
from comments.models import commentsModel, CommentReplies
from single_channel.models import followersModel
import json
# Create your views here.

def get_post_details(vid_id):

    steem_url = ""
    whale_url = ""
    smoke_url = ""

    try:
        steem = SteemVideo.objects.get(video_id=vid_id)
        steem_url = steem.post_url
        # permalink = steem.permlink
        # author = steem.author
    except Exception as e:
        print('Got Error: {}'.format(str(e)))

    try:
        whale = WhaleShareVideo.objects.get(video_id=vid_id)
        whale_url = whale.post_url
        # permalink = whale.permlink
        # author = whale.author
    except Exception as e: 
        print('Got Error: {}'.format(str(e)))

    try:
        smoke = SmokeVideo.objects.get(video_id=vid_id)
        smoke_url = smoke.post_url
        # permalink = smoke.permlink
        # author = smoke.author

    except Exception as e: 
        print('Got Error: {}'.format(str(e)))

    videoDetails = Video.objects.get(id=vid_id)
    total_dislikes = videoDetails.thumbsDown
    total_likes = videoDetails.thumbsUp
    total_earning = videoDetails.total_earning

    return steem_url, smoke_url, whale_url, total_likes, total_dislikes, total_earning

def index(request, video_hash, video_id):
    if 'display_nsfw' not in request.session:
        request.session['display_nsfw'] = False

    current = Video.objects.get(id=video_id)
    steem_url, smoke_url, whale_url, total_likes, total_dislikes, total_earning = get_post_details(current.id)

    current = Video.objects.get(id=video_id)
    hash = json.loads(current.video)
    resolution = [2160, 1440, 1080, 720, 480, 360, 240  , 144]

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

        if request.session['display_nsfw'] == False:
            featured = Video.objects.filter(nsfw=False).order_by('-id')[:1]
            recommend = Video.objects.filter(nsfw=False).order_by('-views')[:1]
        else:
            featured = Video.objects.all().order_by('-id')[:2]
            recommend = Video.objects.all().order_by('-views')[:2]

        user = User.objects.get(id=current.user_id)
        count = Video.objects.filter(user_id=current.user_id).count()

        bestHash_Featured = []
        bestHash_Recomended = []

        for each_video in featured:
            for each_res in resolution:
                if str(each_res) in each_video.video:
                    hash1 = demjson.decode(each_video.video)
                    each_video.featured = hash1[str(each_res)]
                    break   

        for each_video in recommend:
            for each_res in resolution:
                if str(each_res) in each_video.video:
                    hash1 = demjson.decode(each_video.video)
                    each_video.recommend = hash1[str(each_res)]
                    break   

        
        dump = json.dumps(hash)
        
        video_content = ''

        for quality, this_hash in hash.items():
            video_content = video_content + '{\n\t src: \'https://gateway.ipfs.io/ipfs/' + this_hash + '\',\n\t type: \'video/mp4\',\n\t size: ' + quality + ',\n},\n' 
        
        try:
            chkLike, chkDislike = likedordisliked (request, request.user.id, video_id)
        except:
            chkLike = False
            chkDislike = False

        cmntForm = commentForm()
        all_comments = commentsModel.objects.filter(video = video_id)

        is_following = followersModel.objects.filter(user = request.user.id, following=current.user.id).exists()
        followerscount = followersModel.objects.filter(following=current.user.id).count()
        if request.user.is_authenticated and request.user.id == current.user.id:
                own_channel = True
        else:
                own_channel = False

        return render(request, "watch/base.html", {'video_hash': hash, 'cont': video_content,
        'latest': featured, 'recommended': recommend, 'current': current, 'is_following':is_following,'followerscount':followerscount,'own_channel':own_channel,
        'user': user, 'count': count, 'steem_url': steem_url, 'smoke_url': smoke_url, 'whale_url': whale_url, 'chkLike': chkLike, 'chkDislike':chkDislike,
        'total_likes': total_likes, 'total_dislikes': total_dislikes, 'total_earning': total_earning, 'cmntForm':cmntForm, 'all_comments':all_comments})
    

def likedordisliked (request, user_id, video_id):
    if request.user.is_authenticated:
            likeDislike = Activity.objects.filter(user_id=user_id, video_id = video_id).exists()
            if likeDislike == True:
                checkLikeDislike = Activity.objects.get(user_id=user_id, video_id = video_id)
                chkLike = checkLikeDislike.thumbsUp
                chkDislike = checkLikeDislike.thumbsDown
                return chkLike, chkDislike
            else:
                return False ,False