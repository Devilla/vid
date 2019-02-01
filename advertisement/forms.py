from django import forms
from advertisement.models import advertisement

class advertisementForm(forms.Form):
    ad_title = forms.CharField(
        label="Advertisement Title",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title of your advertisement for you to know'})
    )

    total_plays = forms.IntegerField(
        label="Total Plays",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the number of times the video should be played'})
    )

    targeted_tags = forms.CharField(label="Targeted tags",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seperated by comma'}))

    ad_banner = forms.FileField(
        label="Advertisement Banner",
        required=True,
        widget=forms.TextInput(attrs={'id': 'c-cover', 'placeholder': 'Enter the banner. Recommended with is 480'})
    )

    class Meta:
        model = advertisement
        fields = ('ad_title', 'total_plays', 'targeted_tags', 'ad_banner')