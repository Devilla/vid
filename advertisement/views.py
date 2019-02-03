from django.shortcuts import render, redirect
from .forms import advertisementForm
from .models import advertisement
from upload.models import Video
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
def index(request):
    af = advertisementForm()
    if request.method == 'POST':
        af = advertisementForm(request.POST, request.FILES)

        if af.is_valid():
            myfile = request.FILES['ad_banner']
            fs = FileSystemStorage()
            filename = fs.save(os.path.join("static/ads", myfile.name), myfile)
            uploaded_file_url = fs.url(filename)

            raw_tags = af.cleaned_data['targeted_tags'].replace(' ',',').split(',')
                    
            splitted_tags = [x.strip() for x in raw_tags if x.strip()!= ""]
            
            col = advertisement(user=request.user, ad_title=af.cleaned_data['ad_title'], ad_banner=uploaded_file_url, total_plays=af.cleaned_data['total_plays'], targeted_tags=splitted_tags)
            col.save()

            print(col.id)

            return redirect('create.html:Active')
    else:
        all_tags = ([i for i in Video.objects.values_list('tags', flat=True)])
        flat_list = [item for sublist in all_tags for item in sublist]
        flat_list = list(set(list(filter(None, flat_list)))) 

        return render(request, "advertisement/create.html", context={'af': af, 'available_tags': flat_list})