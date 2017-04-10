from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings

def index(request):
   messages.info(request, 'Three credits remain in your account.')
   content = "Hello Alex!!! You future salary is - 4500$!!!It is very cool!!!Be happy!!!"
   storage = messages.get_messages(request)
   d = []
   for message in storage:
      d.append(message)
   return HttpResponse(d)
