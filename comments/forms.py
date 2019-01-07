from django import forms
from.models import commentsModel

class commentForm(forms.ModelForm):
     class Meta:
        model = commentsModel
        fields = ('comment','video')
        comment = forms.CharField(widget=forms.Textarea, label="Write a comment...")
        widgets = {
            'video': forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'display:none'}),
        }

