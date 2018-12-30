from django import forms

class videoLikeForm(forms.Form):
    likevideoID = forms.CharField(
        label="videoID",
        required=True,
        widget=forms.HiddenInput(),
    )

class videoDisLikeForm(forms.Form):
    dislikevideoID = forms.CharField(
        label="videoID",
        required=True,
        widget=forms.HiddenInput(),
    )