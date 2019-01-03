from django import forms

class postOptionsForm(forms.Form):
    name = forms.CharField(label='Name', required=True, max_length=200)
    steem = forms.BooleanField(required = False)
    whale = forms.BooleanField(required = False)
    smoke = forms.BooleanField(required = False)
    duration = forms.CharField(max_length=10)
    tags = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    language_choices = [(1,'English'),(2,'Chinese'), (3,'Spanish'), (4,'German')]
    language = forms.ChoiceField(choices=language_choices,  widget=forms.Select(), required=True)