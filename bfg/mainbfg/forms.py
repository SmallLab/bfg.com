from django import forms
from mainbfg.models import Sentence

class RegistrationsForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, error_messages={'required': 'Введите логин',
                                                                            'min_length':'Логин должен содержать не менее 5-и символов',
                                                                            'max_length': 'Логин должен содержать не более 20-и символов'})

    password = forms.CharField(max_length=20, min_length=8, error_messages={'required':'Введите пароль',
                                                                            'min_length':'Пароль должен содержать не менее 8-и символов',
                                                                            'max_length': 'Пароль должен содержать не более 20-и символов'
                                                                            })



class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, error_messages={'required': 'Введите логин',
                                                                            'min_length': 'Логин должен содержать не менее 5-и символов',
                                                                            'max_length': 'Логин должен содержать не более 20-и символов'})

    password = forms.CharField(max_length=20, min_length=8, error_messages={'required': 'Введите пароль',
                                                                            'min_length': 'Пароль должен содержать не менее 8-и символов',
                                                                            'max_length': 'Пароль должен содержать не более 20-и символов'
                                                                            })
