from django.shortcuts import render, HttpResponse
from upload.models import Video, SteemVideo, WhaleShareVideo, SmokeVideo
from register.models import User
import demjson
from like_dislike.models import Activity
from single_channel.models import followersModel
import json
from datetime import datetime, timedelta
from django_pandas.io import read_frame


def get_similarity_percentage(x, parent_tags):
    same_items = len(set(x) & set(parent_tags))
    total_items = len(x)

    similarity_percentage = 0

    try:
        similarity_percentage = same_items/total_items
    except:
        pass

    return similarity_percentage

def get_recommended_videos(all_vids, parent_tags):
    df = read_frame(all_vids).reset_index(drop=True)

    df['similarity'] = df['tags'].apply(get_similarity_percentage, args=(parent_tags, ))
    df = df.sort_values('similarity', ascending=False)
    
    df = df.drop('similarity', axis=1)

    recommended_videos=[]

    for idx, row in df.iterrows():
        curr_object = Video.objects.get(id=row['id'])

        hashes = json.loads(curr_object.video)
        curr_object.url = "/watch/{}/{}/".format(list(hashes.values())[0], curr_object.id)
        recommended_videos.append(curr_object)

    return recommended_videos[:10]

def GetTime(seconds):
    sec = timedelta(seconds=seconds)
    d = datetime(1,1,1) + sec

    return d.day-1, d.hour, d.minute, d.second

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

    if 'light_on' not in request.session:
        request.session['light_on'] = False
        
    if 'autoplay' not in request.session:
        request.session['autoplay'] = False

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
            all_vids = Video.objects.filter(nsfw=False)
        else:
            featured = Video.objects.all().order_by('-id')[:2]
            all_vids = Video.objects.all()



        recommend = get_recommended_videos(all_vids, list(current.tags))
        up_next = recommend[:1]
        recommend = recommend[1:]

        user = User.objects.get(id=current.user_id)
        count = Video.objects.filter(user_id=current.user_id).count()
        
        video_content = ''

        for quality, this_hash in hash.items():
            video_content = video_content + '{\n\t src: \'https://gateway.ipfs.io/ipfs/' + this_hash + '\',\n\t type: \'video/mp4\',\n\t size: ' + quality + ',\n},\n' 
        
        try:
            chkLike, chkDislike = likedordisliked (request, request.user.id, video_id)
        except:
            chkLike = False
            chkDislike = False

        is_following = followersModel.objects.filter(user = request.user.id, following=current.user.id).exists()
                

        try:
            followerscount = followersModel.objects.get(following=current.user.id).total_followers
        except:
            followerscount = 0 

        print("The followerscount is {}".format(followerscount))

        if request.user.is_authenticated and request.user.id == current.user.id:
                own_channel = True
        else:
                own_channel = False

        time_difference = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()) - int(current.uploaded_at.strftime("%s"))
        day, hour, minute, second = GetTime(time_difference)

        if day >= 30:
            uploaded_time = "{} month ago".format(int(day/30))
        elif day >= 1:
            uploaded_time = "{} day ago".format(day)
        elif hour >= 1:
            uploaded_time = "{} hour ago".format(hour)
        elif minute >= 1:
            uploaded_time = "{} minute ago".format(minute)
        else:
            uploaded_time = "{} second ago".format(second)
        

        return render(request, "watch/base.html", {'video_hash': hash, 'cont': video_content,
        'latest': featured, 'recommended': recommend, 'up_next':up_next, 'current': current, 'is_following':is_following,'followerscount':followerscount,'own_channel':own_channel,
        'user': user, 'count': count, 'steem_url': steem_url, 'smoke_url': smoke_url, 'whale_url': whale_url, 'chkLike': chkLike, 'chkDislike':chkDislike,
        'total_likes': total_likes, 'total_dislikes': total_dislikes, 'total_earning': total_earning, 'uploaded_time': uploaded_time})
    

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