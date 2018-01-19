from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from mainbfg.mainhelpers.modelhelpers import ModelHelpers
from mainbfg.models import Sentence

"""
    Class MainView  - start page
"""

class MainView(TemplateView):

   template_name = 'index.html'

   def get_context_data(self, **kwargs):
       context = super(MainView, self).get_context_data(**kwargs)
       context['data_ctr'] = ModelHelpers.get_data_ctr()
       context['sentences_list'] = ModelHelpers.get_top_sentences()
       return context

"""
    Class ViewSentence - view single sentence
"""

class ViewSentence(DetailView):
    template_name = 'sentences/viewsentence.html'
    slug_field = 'identifier'
    model = Sentence
    context_object_name = 'sentence'

    def get(self, request, *args, **kwargs):
        """
        Increase offer count
        """
        obj = self.get_object()
        obj.views += 1
        obj.save()
        return DetailView.get(self, request, *args, **kwargs)
