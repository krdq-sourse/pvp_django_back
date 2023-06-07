from django import forms
from .models import *

class UserOpenProfile(forms.Form):
    steamID = forms.CharField(max_length=64, label='ID игрока')

class UserDonate(forms.Form):
    coins = forms.IntegerField(label="Монет", max_value=100000)
    id = forms.CharField(widget = forms.HiddenInput())