from django.shortcuts import render

# Create your views here.

def mychannel(request):
    if request.method == 'GET':
        return render(request, 'channel/mychannel.html')