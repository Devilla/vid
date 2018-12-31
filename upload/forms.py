from django import forms

class postOptionsForm(forms.Form):
    name = forms.CharField(label='Name', required=True, max_length=200)
    steem = forms.BooleanField(required = False)
    whale = forms.BooleanField(required = False)
    smoke = forms.BooleanField(required = False)