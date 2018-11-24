from django.shortcuts import render, redirect
from django.contrib.auth import logout
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        logout(request)
        return redirect('/')