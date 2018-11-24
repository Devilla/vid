from django import forms
from register.models import User
from django.contrib.auth import authenticate, login, logout


class userLoginForm(forms.Form):
    email = forms.EmailField(
        label="Your Email Address",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'sample@gmail.com'})
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError("Incorrect username or password")
        elif not user.is_active:
            raise forms.ValidationError("This user is no longer active.")
        return super(userLoginForm, self).clean(*args, **kwargs)