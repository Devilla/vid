from django.shortcuts import render
from upload.forms import postOptionsForm
from register.models import User

def upload(request):
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