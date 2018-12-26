from django import forms
from register.models import User
from django.contrib.auth.forms import UserCreationForm

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

class UserBlockChainForm(forms.Form):

    smoke = forms.CharField(
        label="Smoke Id",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Smoke Id'})
    )
    
    steem = forms.CharField(
        label="Steem Id",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Steem Id'})
    )
    
    whaleshare = forms.CharField(
        label="Whaleshare Id",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Whaleshare Id'})
    )
    
    smoke_name = forms.CharField(
        label="Smoke Name",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Smoke Name'})
    )

    steem_name = forms.CharField(
        label="Steem Name", 
        required=False,                  
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Steem Name'})
    )

    whaleshare_name = forms.CharField(
        label="Whaleshare name",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Whaleshare Name'})
    )

    class Meta:
        model = User
        fields = ('smoke', 'steem', 'whaleshare', 'smoke_name', 'steem_name', 'whaleshare_name')


    def clean_smoke(self):
        smoke = self.cleaned_data['smoke']
        return smoke
    
    def clean_steem(self):
        steem = self.cleaned_data['steem']
        return steem

    def clean_whaleshare(self):
        whaleshare = self.cleaned_data['whaleshare']
        return whaleshare

    def save(self, data, id):
        u = User.objects.get(id = id)
        u.smoke = data['smoke']
        u.steem = data['steem']
        u.whaleshare = data['whaleshare']
        u.smoke_name = data['smoke_name']
        u.steem_name = data['steem_name']
        u.whaleshare_name = data['whaleshare_name']

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

    channel_picture = forms.FileField(
        label="Channel Picture",
        required=True,
        widget=forms.FileInput(attrs={'id': 'c-picture', 'placeholder': 'Select the profile picture for your channel'})
    )


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'channel_name', 'channel_cover', 'profile_picture', 'channel_picture', 'smoke', 'steem', 'whaleshare', 'smoke_name', 'steem_name', 'whaleshare_name')

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
        u.channel_picture = data['channel_picture']
        u.smoke = data['smoke']
        u.steem = data['steem']
        u.whaleshare = data['whaleshare']
        u.smoke_name = data['smoke_name']
        u.steem_name = data['steem_name']
        u.whaleshare_name = data['whaleshare_name']

        u.save()
        return True