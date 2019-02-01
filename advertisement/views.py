from django.shortcuts import render
from .forms import advertisementForm
from upload.models import Video
# Create your views here.
def index(request):
    af = advertisementForm()

    all_tags = ([i for i in Video.objects.values_list('tags', flat=True)])
    flat_list = [item for sublist in all_tags for item in sublist]
    flat_list = list(set(list(filter(None, flat_list)))) 

    return render(request, "advertisement/create.html", context={'af': af, 'available_tags': flat_list})