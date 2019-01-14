from django import forms
from register.models import User
from django.contrib.auth.forms import UserCreationForm
from beem import Steem

class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(
        label="Your Email Address",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'sample@gmail.com'})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re type Password'})
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email1 = self.cleaned_data['email']
        if User.objects.filter(email=email1).exists():
            raise forms.ValidationError(
                'This email address is already in use.')
        else:
            return email1

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError("Password do not match.")
        return password2

    def save(self, datas):
        u = User.objects.create_user(email = datas['email'],
                                     password = datas['password1'])
        u.save()
        return True

class SmokeBlockChainForm(forms.Form):

    smoke = forms.CharField(
        label="Smoke Posting Key",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Smoke Posting Key'})
    )
    
    smoke_name = forms.CharField(
        label="Smoke Username",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Smoke Username'})
    )

    class Meta:
        model = User
        fields = ('smoke', 'smoke_name')


    def clean_smoke(self):
        smoke = self.cleaned_data['smoke']
        return smoke
    
    def save(self, data, id):
        u = User.objects.get(id = id)
        u.smoke = data['smoke']
        u.smoke_name = data['smoke_name']
    
        u.save()
        return True

class WhaleBlockChainForm(forms.Form):

    whaleshare = forms.CharField(
        label="Whaleshare Posting Key",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Whaleshare Posting Key'})
    )
    
    whaleshare_name = forms.CharField(
        label="Whaleshare Username",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Whaleshare Username'})
    )

    class Meta:
        model = User
        fields = ('whaleshare', 'whaleshare_name')


    def clean_whaleshare(self):
        whaleshare = self.cleaned_data['whaleshare']
        return whaleshare

    def save(self, data, id):
        u = User.objects.get(id = id)
        u.whaleshare = data['whaleshare']
        u.whaleshare_name = data['whaleshare_name']

        u.save()
        return True


class SteemBlockChainForm(forms.Form):

    steem = forms.CharField(
        label="Steem Posting Key",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Steem Posting Key'})
    )
    
    steem_name = forms.CharField(
        label="Steem Username", 
        required=False,                  
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Steem Username'})
    )

    class Meta:
        model = User
        fields = ('steem', 'steem_name')


    def clean_steem(self):
        steem = self.cleaned_data['steem']
        
        try:
            s = Steem(keys=[steem], nodes=["https://api.steemit.com", "https://rpc.buildteam.io"])
            if s.is_connected():
                return steem
            else:
                raise forms.ValidationError('This is an invalid key')
        except:
             raise forms.ValidationError('This is an invalid key')

        

    def save(self, data, id):
        u = User.objects.get(id = id)
        u.steem = data['steem']
        u.steem_name = data['steem_name']

        u.save()
        return True


class UserRegistrationCompletionForm(forms.Form):

    first_name = forms.CharField(
        label="First name",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )

    last_name = forms.CharField(
        label="Surname",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )

    channel_name = forms.CharField(
        label="Channel Name",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Channel Name'})
    )

    channel_cover = forms.FileField(
        label="Channel Cover",
        required=True,
        widget=forms.FileInput(attrs={'id': 'c-cover', 'placeholder': 'Select the cover image for your channel'})
    )

    profile_picture = forms.FileField(
        label="Profile Picture",
        required=True,
        widget=forms.FileInput(attrs={'id': 'p-picture', 'placeholder': 'Select the profile picture for your account'})
    )

    # channel_picture = forms.FileField(
    #     label="Channel Picture",
    #     required=True,
    #     widget=forms.FileInput(attrs={'id': 'c-picture', 'placeholder': 'Select the profile picture for your channel'})
    # )


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'channel_name', 'channel_cover', 'profile_picture', 'smoke', 'steem', 'whaleshare', 'smoke_name', 'steem_name', 'whaleshare_name')

    def clean_first(self):
        first_name = self.cleaned_data['first_name']
        return first_name
    
    def clean_last(self):
        last_name = self.cleaned_data['last_name']
        return last_name

    def clean_channel(self):
        channel_name = self.cleaned_data['channel_name']
        return channel_name


    def save(self, data, id):
        print(id)
        u = User.objects.get(id = id)
        u.first_name = data['first_name']
        u.last_name = data['last_name']
        u.channel_name = data['channel_name']
        u.channel_cover = data['channel_cover']
        u.profile_picture = data['profile_picture']
    
        u.save()
        return True