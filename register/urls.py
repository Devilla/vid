from django.urls import path, re_path
from django.conf.urls import url
from register.views import index, update, steem_blockchain, smoke_blockchain, whale_blockchain

app_name = 'register'

urlpatterns = [
    path('', index, name="register"),
    path('update/', update, name="update"),
    path('steem_blockchain/', steem_blockchain, name="steem_blockchain"),
    path('smoke_blockchain/', smoke_blockchain, name="smoke_blockchain"),
    path('whale_blockchain/', whale_blockchain, name="whale_blockchain"),

]
