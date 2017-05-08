from django.shortcuts import redirect, render_to_response
from mainbfg.forms import RegistrationsForm

def registrationUser(request):
    if request.method == 'POST':
        form = RegistrationsForm(request.POST)
    if form.is_valid():
        form.save()  # save user to database if form is valid
        return redirect('/')
    else:
        return render_to_response('registration/login.html', {"errors": form.errors, 'info':request.POST})