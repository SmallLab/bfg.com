from django.shortcuts import redirect, render_to_response
from mainbfg.forms import RegistrationsForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

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
        return render_to_response('registration/login.html', {"errors": form.errors,
                                                              'info':request.POST,
                                                              'tab':True
                                                              })
    else:
        return render_to_response('registration/login.html', {"errors": form.errors,
                                                              'info': request.POST,
                                                              'tab': True
                                                              })