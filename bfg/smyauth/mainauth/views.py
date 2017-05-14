import requests
from django.shortcuts import redirect, render_to_response
from django.conf import settings
from django.views.generic import View
from django.contrib import messages

"""
    Facebook Autentification
"""

class FacebookAuth(View):

    def get(self, request):
        access_token = self.get_access_token()
        if access_token['status']:
            facebook_data = self.get_facebook_data(access_token['access_token'])
            if facebook_data['status']:
                return render_to_response('registration/login.html', {'userf':facebook_data})
            else:
                return render_to_response('registration/login.html', {'failauth': True})
        else:
            return render_to_response('registration/login.html', {'failauth': True})

    def get_access_token(self):
        code = self.request.GET.get('code', '')
        try:
            graph_url = requests.get(settings.FACEBOOK_GRAF_URL, {'client_id': settings.FACEBOOK_APP_ID,
                                                                  'redirect_uri': settings.FACEBOOK_REDIRECT_URL,
                                                                  'client_secret': settings.FACEBOOK_SECRET,
                                                                  'code': code})
            if 'error' in graph_url.json():
                return {'status':False}
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

    def create_new_user(self, facebook_data):
        pass