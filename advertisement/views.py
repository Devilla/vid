from django.shortcuts import render, redirect
from .forms import advertisementForm
from .models import advertisement
from upload.models import Video
from django.core.files.storage import FileSystemStorage
import os

from bitshares import BitShares
import os
from bitshares.account import Account
from bitshares.memo import Memo
import threading
import time
import uuid

from datetime import datetime

tasks = {}

# Create your views here.
def index(request):
    if request.user.is_authenticated == True:
        all_tags = ([i for i in Video.objects.values_list('tags', flat=True)])
        flat_list = [item for sublist in all_tags for item in sublist]
        flat_list = list(set(list(filter(None, flat_list)))) 

        af = advertisementForm()
        activeAds = []
        inactiveAds = []
        for ad in advertisement.objects.all():
            if ad.user == request.user:
                if ad.paid == True:
                    if ad.active == True:
                        activeAds.append(ad)
                    else:
                        inactiveAds.append(ad)

        print(activeAds)
        print(inactiveAds)

        

        if request.method == 'POST':
            af = advertisementForm(request.POST, request.FILES)

            if af.is_valid():
                myfile = request.FILES['ad_banner']
                fs = FileSystemStorage()
                filename = fs.save(os.path.join("static/ads", myfile.name), myfile)
                uploaded_file_url = fs.url(filename)

                raw_tags = af.cleaned_data['targeted_tags'].replace(' ',',').split(',')
                        
                splitted_tags = [x.strip() for x in raw_tags if x.strip()!= ""]
                
                payment_amount = int(af.cleaned_data['total_plays']) / 10

                col = advertisement(user=request.user, ad_title=af.cleaned_data['ad_title'], ad_banner=uploaded_file_url, total_plays=af.cleaned_data['total_plays'], targeted_tags=splitted_tags, amount=payment_amount, memo=uuid.uuid4().hex[:16])
                col.save()

                request.session['current_payment_info'] = col.id
                return redirect("pay.html")
        else:
            
            return render(request, "advertisement/create.html", context={'af': af, 'available_tags': flat_list, 'show': 'homepage', 'active_ads': activeAds, 'inactive_ads': inactiveAds})
    else:
        return redirect('/login')

pass_phrase = "OKFjkrk3412"

owner_key = "5JrC9FxgxtJ8fi8UjPgL57KH27ToVngEZ7Aka6uSSNBFb2XTVgB"
memo_key = "5KUVfh5zagFRheVT8G4PQXjknw25nuEXizsh3k3JhY3J5cEkq1H"
active_key = "5JyorRk13HM1WDJ4VvPE7WimPa4KB21qhLQMTcuZkNxBdafdQnV"

bitshares = BitShares(node=["wss://openledger.hk/ws", "wss://us.nodes.bitshares.ws", "wss://bitshares.openledger.info/ws"])

try:
    bitshares.wallet.create(pass_phrase)
    bitshares.wallet.addPrivateKey(owner_key)
    bitshares.wallet.addPrivateKey(active_key)
    bitshares.wallet.addPrivateKey(memo_key)
except:
    bitshares.wallet.unlock(pass_phrase)

acc = bitshares.wallet.getAccounts()[0]['account']
m = Memo(blockchain=bitshares)
m.blockchain.wallet.unlock(pass_phrase)

def verify_transaction(acc, m, to_send_text, to_send_amount, payment_id, loop_time):
    starting_time = time.time()

    while True:
        started_time = time.time() - starting_time
        if started_time > loop_time:
            break

        ad_object = advertisement.objects.get(id=payment_id)

        for transaction in acc.history():
            currInfo = transaction['op'][1]

            if 'to' in currInfo:
                valid = currInfo
                if(currInfo['to'] == acc.identifier):
                    amount = currInfo['amount']['amount']/100
                    memo = m.decrypt(valid['memo'])
                    
                    if int(to_send_amount) == int(amount) and to_send_text == memo:
                        ad_object.paid = True
                        ad_object.save()
                        break

        time.sleep(2)
        print("Not found yet")

def pay(request):
    global acc
    global m
    global tasks

    ad_object = advertisement.objects.get(id=request.session['current_payment_info'])
    memo = ad_object.memo
    amount = ad_object.amount
    is_paid = ad_object.paid

    payment_status = "NOT PAID"

    if (is_paid == True):
        payment_status = "PAID"
        ad_object.paid = True
        if ad_object.total_plays < ad_object.currently_played:
            ad_object.active = True
            ad_object.save()

    remaining_time = (int(ad_object.curr_time.strftime("%s")) + (3 * 60 * 60)) - int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())

    if str(request.user.id) not in tasks:
        tasks[str(request.user.id)] = threading.Thread(target=verify_transaction, args=(acc, m, memo, amount, request.session['current_payment_info'],remaining_time,))

    if tasks[str(request.user.id)].isAlive() == False:
        tasks[str(request.user.id)].start()
    
    if remaining_time <= 0:
        ad_object.active = True
        ad_object.save()
        return redirect("create.html")
    else:
        if payment_status == "PAID":
            return redirect("/advertisement")
        else:
            return render(request, "advertisement/pay.html", context={'amount': amount,'memo': memo, 'payment_status': payment_status, 'remaining_time': remaining_time})