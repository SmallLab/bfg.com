import re

from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf
from mainbfg.forms import RegistrationsForm, LoginForm

"""
    Registrations new user
"""


def RegistrationUser(request):
  if request.method == 'POST':
    form = RegistrationsForm(request.POST)
    isset_user_login = User.objects.filter(username=request.POST['username'])
    if form.is_valid() and not isset_user_login:
      new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                          password=form.cleaned_data['password'])
      new_user.save()
      user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
      if user is not None:
        if user.is_active:
          login(request, user)
          if request.POST['sub_id']:
            return redirect(request.POST['next_url'] + '&sub_id=' + request.POST['sub_id'])
          else:
            return redirect(request.POST['next_url'])
        else:
          return redirect('/login/')
      else:
        return redirect('/login/')
    elif form.is_valid() and isset_user_login:
      form.errors.username = 'Пользователь с таким логином уже существует, выберите другой логин'
      c = {"rerrors": form.errors, 'tab': True, 'next_url': request.POST['next_url'], 'sub_id': request.POST['sub_id']}
      c.update(csrf(request))
      return render(request, 'registration/login.html', c)
    else:
      c = {"rerrors": form.errors, 'tab': True, 'next_url': request.POST['next_url'], 'sub_id': request.POST['sub_id']}
      c.update(csrf(request))
      return render(request, 'registration/login.html', c)
  else:
    c = {'tab': True}
    if request.GET:
      if request.GET.get('id_sent'):
        next_u = request.get_full_path().split('&')[0:-1]
        c['next_url'] = '&'.join(next_u)[13:]
        c['sub_id'] = request.get_full_path().split('&').pop()
      else:
        c['next_url'] = request.get_full_path()[13:]
        c['sub_id'] = ''
    else:
      c['next_url'] = '/user/privateoffice/'
    c.update(csrf(request))
    return render(request, 'registration/login.html', c)


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
          if request.POST['sub_id']:
            return redirect(request.POST['next_url'] + '&sub_id=' + request.POST['sub_id'])
          else:
            return redirect(request.POST['next_url'])
        else:
          return redirect('/login/')
      else:
        none_user = 'Пользователя с таким логином и паролем не существует!!!'
        c = {"none_user": none_user, 'tab': False, 'next_url': request.POST['next_url'],
             'sub_id': request.POST['sub_id']}
        c.update(csrf(request))
        return render(request, 'registration/login.html', c)
    else:
      c = {"lerrors": login_form.errors, 'tab': False, 'next_url': request.POST['next_url'],
           'sub_id': request.POST['sub_id']}
      c.update(csrf(request))
      return render(request, 'registration/login.html', c)
  else:
    c = {'tab': False}
    c.update(csrf(request))
    if request.GET:
      if request.GET.get('id_sent'):
        next_u = request.get_full_path().split('&')[0:-1]
        c['next_url'] = '&'.join(next_u)[13:]
        c['sub_id'] = request.get_full_path().split('&').pop()[8:]
      else:
        c['next_url'] = request.get_full_path()[13:]
        c['sub_id'] = ''
    else:
      c['next_url'] = '/user/privateoffice/'
    return render(request, 'registration/login.html', c)
