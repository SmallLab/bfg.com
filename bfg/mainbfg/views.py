from django.shortcuts import redirect, render_to_response
from mainbfg.forms import RegistrationsForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf

"""
    Registrations new user
"""

def RegistrationUser(request):
    if request.method == 'POST':
        form = RegistrationsForm(request.POST)
        isset_user_login = User.objects.filter(username=request.POST['username'])
        if form.is_valid() and not isset_user_login:
            new_user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return redirect('/login/')
            else:
                return redirect('/login/')
        elif form.is_valid() and isset_user_login:
            form.errors.username = 'Пользователь с таким логином уже существует, выберите другой логин'
            c = {"rerrors": form.errors, 'tab': True, }
            c.update(csrf(request))
            return render_to_response('registration/login.html', c)
        else:
            c = {"rerrors": form.errors, 'tab': True,}
            c.update(csrf(request))
            return render_to_response('registration/login.html', c)
    else:
        c = {'tab': True}
        c.update(csrf(request))
        return render_to_response('registration/login.html', c)

"""
    Login user
"""

def LoginUser(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return redirect('/login/')
            else:
                none_user = 'Пользователя с таким логином и паролем не существует!!!'
                c = {"none_user": none_user, 'tab': False}
                c.update(csrf(request))
                return render_to_response('registration/login.html', c)
        else:
            c = {"lerrors": login_form.errors, 'tab': False,}
            c.update(csrf(request))
            return render_to_response('registration/login.html', c)
    else:
        c = {'tab':False}
        c.update(csrf(request))
        return render_to_response('registration/login.html', c)