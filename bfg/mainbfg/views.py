from django.shortcuts import render

from django.http import HttpResponse
import datetime

def index(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
    #return HttpResponse("Hello Alex!!! You future salary is - 3500$!!!It is very cool!!!Be happy!!!")
