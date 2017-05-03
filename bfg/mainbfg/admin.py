from django.contrib import admin
from .models import TypeSentence, Categories, Regions
from django.contrib.auth.models import Permission

admin.site.register(Permission)

admin.site.register(TypeSentence)
admin.site.register(Categories)
admin.site.register(Regions)