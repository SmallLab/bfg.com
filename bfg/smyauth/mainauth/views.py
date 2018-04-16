import requests
import logging

from django.shortcuts import redirect, render_to_response
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.template.context_processors import csrf
from mainbfg.models import Profile

"""
    Facebook Autentification
"""
class DataGet():
    next_url=''

def getF(request):
    DataGet.next_url = request.get_full_path()[30:]
    # logfb = logging.getLogger(__name__)
    # logfb.error(request.get_full_path()[30:])
    return redirect(settings.FACEBOOK_URL)

class FacebookAuth(RedirectView):

    def get(self, request):
        access_token = self.get_access_token()
        if access_token['status']:
            facebook_data = self.get_facebook_data(access_token['access_token'])
            if facebook_data['status']:
                try:
                    profile = Profile.objects.get(facebook_id=facebook_data['user_data']['id'])
                except Profile.DoesNotExist:
                    user = self.create_new_user(facebook_data['user_data'])
                else:
                    user = profile.user
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect(DataGet.next_url)
                    else:
                        return self.bad_status(request)
                else:
                    return self.bad_status(request)
            else:
                return self.bad_status(request)
        else:
            return self.bad_status(request, access_token['data'])

    def get_access_token(self):
        code = self.request.GET.get('code', '')
        try:
            graph_url = requests.get(settings.FACEBOOK_GRAF_URL, {'client_id': settings.FACEBOOK_APP_ID,
                                                                  'redirect_uri': settings.FACEBOOK_REDIRECT_URL,
                                                                  'client_secret': settings.FACEBOOK_SECRET,
                                                                  'code': code})
            if 'error' in graph_url.json():
                return {'status':False, 'data':graph_url.json()}
            else:
                return {'status':True, 'access_token':graph_url.json()['access_token']}

        except (requests.RequestException, requests.ConnectionError, requests.HTTPError):
            return {'status':False}


    def get_facebook_data(self, access_token):
        try:
            user_data = requests.get(settings.FACEBOOK_USERDATA_URL, {'access_token': access_token})
            return {'status':True, 'user_data':user_data.json()}

        except (requests.RequestException, requests.ConnectionError, requests.HTTPError):
            return {'status':False}


#When created a new user automatically created a record in Profile table for user(look signals/handlers)

    def create_new_user(self, facebook_data):
        username = facebook_data.get('first_name', 'Anonim')
        password = User.objects.make_random_password()
        user = User(
            username=username,
            email=facebook_data.get('email', ''),
            is_staff=False,
            is_active=True,
            is_superuser=False,
       )
        user.set_password(password)
        user.save()

        profile = user.profile
        profile.facebook_id = facebook_data['id']
        profile.first_name = facebook_data.get('first_name', 'Anonim')
        profile.email=facebook_data.get('email', '')
        profile.save()
        return user

    def bad_status(self, request, data=0):
        c = {'failauth': True, 'message_auth': settings.AUTH_FAILED_MESSAGESS+'---'+data}
        c.update(csrf(request))
        logfb = logging.getLogger(__name__)
        logfb.error(data)
        return render_to_response('registration/login.html', c)