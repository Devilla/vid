from django.shortcuts import render, redirect
from login.forms import userLoginForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated == True:
            return redirect('/')
        else:
            form = userLoginForm()
            return render(request, "login/signin.html", {"form": form})
    # return render(request, "login/signin.html", {})
    if request.method == 'POST':
        if request.user.is_authenticated == True:
            return redirect('/')
        else:
            form = userLoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("email")
                pword = form.cleaned_data.get('password')
                user = authenticate(email=email, password=pword)
                login(request, user)
                if login:
                    return redirect('/')
                else:
                    return render(request, "login/signin.html")
        return render(request, "login/signin.html", {"form": form})
