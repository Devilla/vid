from django.shortcuts import render, redirect
from upload.forms import postOptionsForm
from register.models import User
from upload.models import Video, SteemVideo, WhaleShareVideo, SmokeVideo
from beem import Steem
from beem.comment import Comment
from steem import Steem as SteemOriginal
import uuid
import json

def get_unique_permlink(title):
    title=title.lower()
    title = title.replace(" ", "-")
    uid = uuid.uuid4()
    title = title + "-" + uid.hex[:8]
    print("The unique title is: {}".format(title))
    return title

def record(request):
    return render(request, 'livestream/record.html', context={'stream_id': request.session['stream_id'], 'stream_title': request.session['stream_name']})

def upload(request):

    if request.method == "POST":
        optform = postOptionsForm(request.POST)
        
        if optform.is_valid():
            raw_tags = optform.cleaned_data['video_tags'].replace(' ',',').split(',')
            splitted_tags = [x.strip() for x in raw_tags if x.strip()!= ""]
            tags = ['vidsocial'] + splitted_tags
            
            live_video = {}
            live_video['identifier'] = uuid.uuid4().hex[:8]

            steemPost = optform.cleaned_data['steem']
            smokePost = optform.cleaned_data['smoke']
            whalePost = optform.cleaned_data['whale']
            description = optform.cleaned_data['description']
            language = optform.cleaned_data['language']
            name = optform.cleaned_data['name']

            thumbnail_url = 'https://gateway.ipfs.io/ipfs/QmWdE9UVgWGFncQSmEQdvATXF4CYBYqZGKS8Fe3wFGADUv'
            arb_url = 'https://vidsocial.org/watch/live/'+ live_video['identifier'] + '/'

            body = get_body(thumbnail_url, arb_url, description)
            print(steemPost)
            print(smokePost)
            print(whalePost)
            print(body)

            video = Video(user=request.user, type="live", views=0, duration="LIVE", description=description, language=language, tags=tags, name=name, publish=True, monetize=optform.cleaned_data['monetize'], nsfw=optform.cleaned_data['nsfw'],thumbsUp=0, thumbsDown=0, video=json.dumps(live_video), user_id=request.user.id, thumbNail="QmWdE9UVgWGFncQSmEQdvATXF4CYBYqZGKS8Fe3wFGADUv")
            video.save()

            if steemPost == True and request.user.steem != 'false' and request.user.steem_name != 'false':
                    try:
                        print("Steem: {} Steem Name: {}".format(request.user.steem, request.user.steem_name))
                        try:
                            s_res = post_steem(request.user.steem, request.user.steem_name, tags, name, body)
                        except Exception as e:
                            print("error in posting: {}".format(str(e)))
                            # permlink=get_unique_permlink(name)
                            s_res = post_steem(request.user.steem, request.user.steem_name, tags, name, body, benificiary=False)
                        
                        save_data(s_res, 'steem', video.id, tags)
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
                    
                    save_data(wls_res, 'whale', video.id, tags)
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


                    
                    save_data(smk_res, 'smoke', video.id, tags)
                except Exception as e:
                    print(str(e))
                    print('Error smoke')
            else:
                print('No smoke')

            request.session['stream_name'] = name
            request.session['stream_id'] = live_video['identifier']

            return redirect('/stream/record/')

    optform = postOptionsForm()
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

    if user.steem == 'false' and user.smoke == 'false' and user.whaleshare == 'false':
        key['allcheck'] = False
    else:
        key['allcheck'] = True

    return render(request, 'livestream/upload.html', context={'postOptionsForm': postOptionsForm, 'keychk':key})

def play(request):

    try:
        requestedStream = request.GET.get('get')
    except:
        requestedStream = "stream1"

    return render(request, 'livestream/play.html', {'requestedStream': requestedStream})


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


def get_body(thumbnail, vidsocial_url, description):
    body = 'Live Streaming on Vidsocial<br/><br/><center><a href="{}" rel="noopener" title="This link will take you away"><img src="{}" width="480" height="360"></a></center><hr><p></p><p>{}</p><hr><a href="{}" rel="noopener" title="This link will take you away"> ▶️ Vidsocial</a></div></div>'.format(vidsocial_url, thumbnail, description, vidsocial_url)
    return body

def post_steem(steem_key, steem_username, tags, title, body, permlink=None, benificiary=False):
    nodelist_one = ['http://appbasetest.timcliff.com/', 'https://rpc.steemliberator.com/', 'http://rpc.steemviz.com/', 'http://rpc.buildteam.io', 'https://api.steemit.com/']

    s = SteemOriginal(keys=[steem_key])
    s_res = s.commit.post(title=title, body=body, author=steem_username, tags=tags, json_metadata={
                                                                                    'extensions': [[0, {
                                                                                        'beneficiaries': [
                                                                                            {'account': 'fiasteemproject', 'weight': 2500},
                                                                                        ]}
                                                                                    ]]
                                                                                })
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
    wls = Steem(node=["https://wls.kennybll.com", "https://rpc.whaleshares.io", "ws://188.166.99.136:8090"], keys=[whaleshares_key])
        
    wls_res = wls.post(title=title, body=body, author=whaleshares_username, tags=tags, permlink=permlink, json_metadata={
                    'extensions': [[0, {
                        'beneficiaries': [
                            {'account': 'fiasteemproject', 'weight': 2500},
                        ]}
                    ]]
                })

    return wls_res