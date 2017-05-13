import urllib
from django.shortcuts import redirect, render_to_response
from django.conf import settings
from django.views.generic import View

"""
    Facebook Autentification
"""

class FacebookAuth(View):

    def get(self, request):
        access_token = self.get_access_token()
        return  access_token

    def get_access_token(self):
        code = self.request.GET.get('code', '')
        graph_url = "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode({
                                                                                        'client_id': settings.FACEBOOK_APP_ID,
                                                                                        'redirect_uri': settings.FACEBOOK_REDIRECT_URL,
                                                                                        'client_secret': settings.FACEBOOK_SECRET,
                                                                                        'code': code})
        #return render_to_response('registration/login.html', {'code':code})

