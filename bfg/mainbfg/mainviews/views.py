from django.views.generic.base import TemplateView
from django.core.cache import cache
from mainbfg.models import (TypeSentence, Categories, Regions, Sentence)

"""
    Class MainView  - start page
"""


class MainView(TemplateView):

   template_name = 'index.html'

   def get_context_data(self, **kwargs):
       context = super(MainView, self).get_context_data(**kwargs)
       context['data'] = self.get_data_ctr()
       return context


   def get_data_ctr(self):
      if cache.get('data_ctr'):
          return cache.get('data_ctr')
      else:
          data = {}
          data['types'] = TypeSentence.objects.get_active_types()
          data['categories'] = Categories.objects.get_active_categories()
          data['categories_list'] = Categories.objects.get_list_categories()
          data['regions'] = Regions.objects.get_all_regions()
          cache.set('data_ctr', data)

          return data