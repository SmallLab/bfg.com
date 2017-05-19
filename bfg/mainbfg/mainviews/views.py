from django.views.generic.base import TemplateView
from mainbfg.models import (TypeSentence, Categories, Regions)

"""
    Class MainView  - start page
"""


class MainView(TemplateView):

   template_name = 'index.html'

   def get_context_data(self, **kwargs):
      context = super(MainView, self).get_context_data(**kwargs)
      context['types'] = TypeSentence.object.get_active_types()
      context['categories'] = Categories.object.get_active_categories()
      context['categories_list'] = Categories.object.get_list_categories()
      context['regions'] = Regions.objects.all()
      return context