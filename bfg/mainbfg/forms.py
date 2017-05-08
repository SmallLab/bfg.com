from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationsForm(UserCreationForm):
    username = forms.CharField(label='Логин', max_length=50)
    #password = forms.CharField(label="Пароль", max_length=50)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')