from django.forms import ModelForm
from django import forms
from .models import Room
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
