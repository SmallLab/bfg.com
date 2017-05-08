from django import forms

class RegistrationsForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, error_messages={'required': 'Введите логин',
                                                                            'min_length':'Логин должен содержать не менее 5-и символов',
                                                                            'man_length': 'Логин должен содержать не более 20-и символов'})

    password = forms.CharField(max_length=20, min_length=8, error_messages={'required':'Введите пароль',
                                                                            'min_length':'Пароль должен содержать не менее 8-и символов',
                                                                            'man_length': 'Пароль должен содержать не более 20-и символов'
                                                                            })