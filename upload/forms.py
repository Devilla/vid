from django import forms

from .models import File

# Model form
class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)

        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control', 'id':'upload', 'style': 'display:none'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        # if ext not in ["jpg", "pdf", "xlsx"]:
        #     raise forms.ValidationError("Only jpg, pdf and xlsx files are allowed.")
        # return cleaned data is very important.
        
        return file

class postOptionsForm(forms.Form):
    name = forms.CharField(label='Name', required=True, max_length=200)
    steem = forms.BooleanField(required = False)
    whale = forms.BooleanField(required = False)
    smoke = forms.BooleanField(required = False)
    monetize = forms.BooleanField(required=False)
    duration = forms.CharField(max_length=10, required=False)
    video_tags = forms.CharField(max_length=100, required=False)
    description = forms.CharField(widget=forms.Textarea)
    language_choices = [(1,'English'),(2,'Chinese'), (3,'Spanish'), (4,'German')]
    language = forms.ChoiceField(choices=language_choices,  widget=forms.Select(), required=True)