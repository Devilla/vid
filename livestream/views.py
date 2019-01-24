from django.shortcuts import render

def upload(request):
    return render(request, 'livestream/record.html')

def play(request):

    try:
        requestedStream = request.GET.get('get')
    except:
        requestedStream = "stream1"

    return render(request, 'livestream/play.html', {'requestedStream': requestedStream})