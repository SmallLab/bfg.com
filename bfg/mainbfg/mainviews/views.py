from django.views.generic.base import TemplateView, View
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from django.shortcuts import render
from django.http import QueryDict

from mainbfg.mainhelpers.modelhelpers import ModelHelpers
from mainbfg.models import Sentence, Categories, TypeSentence

"""
    Class MainView  - start page
"""

class MainView(TemplateView):

   template_name = 'index.html'

   def get_context_data(self, **kwargs):
       context = super(MainView, self).get_context_data(**kwargs)
       context['data_ctr'] = ModelHelpers.get_data_ctr()
       context['sentences_list'] = ModelHelpers.get_top_sentences()
       context['dict'] = Categories.objects.get_dict_categories()
       context['dict1'] = TypeSentence.objects.get_dict_types()
       return context

"""
    Class CategoryPage - transition to the category
"""

class CategoryPage(ListView):
    template_name = 'sentences/categorypage.html'
    context_object_name = 'sentences_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        # return super(CategoryPage, self).get(self, request, *args, **kwargs)
        self.object_list = self.get_queryset(Categories.objects.get_dict_categories()[self.kwargs['link_name']]['id'],
                                             TypeSentence.objects.get_dict_types()[self.kwargs['type']]['id'])
        context = self.get_context_data(object_list=self.object_list)
        copy_get = QueryDict(request.GET.copy().urlencode(), mutable=True)
        context['request_get'] = copy_get.urlencode()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(CategoryPage, self).get_context_data(**kwargs)
        context['data_ctr'] = ModelHelpers.get_data_ctr()
        context['active_tab'] = TypeSentence.objects.get_dict_types()[self.kwargs['type']]['link_name']
        context['path'] = '/'.join(self.request.path.split('/')[0:4])
        context['true_path'] = '/'.join(self.request.path.split('/')[0:5])
        return context

    def get_queryset(self, category_id, type_id):
        return Sentence.objects.get_category_sentences(category_id, type_id)

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

"""
    Class ShowPhone - view phone for sentence
"""

class ShowPhone(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = Sentence.objects.get_phone(self.request.GET['id_sentence'])
        return JsonResponse(data)