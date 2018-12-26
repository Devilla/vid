from django.shortcuts import render, redirect, HttpResponse
from register.forms import UserRegistrationForm, UserRegistrationCompletionForm, UserBlockChainForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from register.models import User
import ipfsapi

# Create your views here.
def index(request):

    if request.method == 'POST':
        if not request.user.is_authenticated:
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                datas = {}
                datas['email'] = form.cleaned_data['email']
                datas['password1'] = form.cleaned_data['password1']

                if form.save(datas):
                    email = form.cleaned_data['email']
                    pword = form.cleaned_data['password1']
                    user = authenticate(email=email, password=pword)
                    login(request, user)

                    return redirect('register:update')

    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = UserRegistrationForm()
        return render(request, "register/signup.html", {'form': form})

def blockchain(request):
    
    if request.user.is_authenticated == True:
        current = User.objects.get(id=request.user.id)

        if request.method = 'POST':
            formb = UserBlockChainForm(request.POST)

            if formb.is_valid():
                data = {}
                data['smoke'] = formb.cleaned_data['smoke']
                data['steem'] = formb.cleaned_data['steem']
                data['whaleshare'] = formb.cleaned_data['whaleshare']
                data['smoke_name'] = formb.cleaned_data['smoke_name']
                data['steem_name'] = formb.cleaned_data['steem_name']
                data['whaleshare_name'] = formb.cleaned_data['whaleshare_name']

                if formb.save(data, current.id):
                    return redirect('/')
                else:
                    print('Database error')    
            else:
                print('The submitted form is not valid')

        formBl = UserBlockChainForm()            
        return render(request, "register/signup_process.html", {'form':formBl})
            
    else:
        form = UserRegistrationForm()
        return render(request, "register/signup.html", {'form': form})

def update(request):
    if request.user.is_authenticated == True:
        current = User.objects.get(id=request.user.id)

        if request.method == 'POST':
            forma = UserRegistrationCompletionForm(request.POST, request.FILES)
            

            api = ipfsapi.connect('127.0.0.1', 5001)
            profile_picture = api.add_bytes(request.FILES['profile_picture'].read())
            channel_cover = api.add_bytes(request.FILES['channel_cover'].read())
            channel_picture = api.add_bytes(request.FILES['channel_picture'].read())
            
            if forma.is_valid():
                data = {}
                data['first_name'] = forma.cleaned_data['first_name']
                data['last_name'] = forma.cleaned_data['last_name']
                data['channel_name'] = forma.cleaned_data['channel_name']
                data['channel_cover'] = channel_cover
                data['profile_picture'] = profile_picture
                data['channel_picture'] = channel_picture

                if forma.save(data, current.id):
                    return redirect('register:blockchain')

                else:
                    print('Database error') 
            else :
                print("The submitted form is not valid")

        formd = UserRegistrationCompletionForm()            
        return render(request, "register/signup_process.html", {'form':formd})

    else:
        form = UserRegistrationForm()
        return render(request, "register/signup.html", {'form': form})
