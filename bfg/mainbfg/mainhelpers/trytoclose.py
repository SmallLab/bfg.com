from django.http import HttpResponse, HttpResponseNotFound

class CheckUsers(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return HttpResponseNotFound('<h1>Page not found</h1>')
