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
       context['sentences'] = Sentence.objects.get(id=25)
       return context


   def get_data_ctr(self):
      if cache.get('data_ctr'):
          return cache.get('data_ctr')
      else:
          data = {}
          data['types'] = TypeSentence.object.get_active_types()
          data['categories'] = Categories.object.get_active_categories()
          data['categories_list'] = Categories.object.get_list_categories()
          data['regions'] = Regions.objects.all()
          cache.set('data_ctr', data)

          return data