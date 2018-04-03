from django.views.generic.base import TemplateView, View
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from django.shortcuts import render
from django.http import QueryDict

from mainbfg.mainhelpers.modelhelpers import ModelHelpers
from mainbfg.models import Sentence, Categories, TypeSentence
from mainbfg.forms import FilterSentencesForm

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
    Class CategoryPage - transition to the category
"""

class CategoryPage(ListView):
    template_name = 'sentences/categorypage.html'
    context_object_name = 'sentences_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset(Categories.objects.get_dict_categories()[self.kwargs['link_name']]['id'],
                                             TypeSentence.objects.get_dict_types()[self.kwargs['type']]['id'])
        context = self.get_context_data(object_list=self.object_list)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(CategoryPage, self).get_context_data(**kwargs)
        context['data_ctr'] = ModelHelpers.get_data_ctr()
        context['active_tab'] = self.kwargs['type']
        context['path'] = '/'.join(self.request.path.split('/')[0:4])
        context['true_path'] = '/'.join(self.request.path.split('/')[0:5])
        context['category_name'] = Categories.objects.get_dict_categories()[self.kwargs['link_name']]['name']
        context['top_category_sent'] = Sentence.objects.get_top_sentences_category_page(
                                                                  Categories.objects.get_dict_categories()[self.kwargs['link_name']]['id'],
                                                                  TypeSentence.objects.get_dict_types()[self.kwargs['type']]['id'])
        return context

    def get_queryset(self, category_id, type_id):
        return Sentence.objects.get_category_sentences(category_id, type_id)

"""
    Class FilterSentences - Filter suggestions
"""
class FilterSentences(ListView):
    template_name = 'sentences/filtersent.html'
    context_object_name = 'sentences_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        """
        If submit search form, add more options to transfer data from the form in context
        """
        form = FilterSentencesForm(request.GET)
        if form.is_valid():
            self.object_list = self.get_queryset(form.cleaned_data.copy())
            context = self.get_context_data(object_list=self.object_list)
            context['data_form'] = form.cleaned_data
            """
               If want change QueryDict add param mutable=True like positional argument
            """
            context['request_get'] = QueryDict(request.GET.copy().urlencode()).urlencode()
            context['top_category_sent'] = Sentence.objects.get_top_sent_filter_page(form.cleaned_data.copy())
            return render(request, self.template_name, context)
        else:
            self.object_list = self.get_queryset(form.cleaned_data.copy())
            context = self.get_context_data(object_list=self.object_list)
            context['form'] = form
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(FilterSentences, self).get_context_data(**kwargs)
        context['data_ctr'] = ModelHelpers.get_data_ctr()
        context['true_path'] = '/'.join(self.request.path.split('/')[0:2])
        return context

    def get_queryset(self, data):
        return Sentence.objects.get_filter_sentences(data)

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
        obj.save(update_fields=['views'])
        return DetailView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        return Sentence.objects.get_sent_for_view()

"""
    Class ShowPhone - view phone for sentence
"""

class ShowPhone(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = Sentence.objects.get_phone(self.request.GET['id_sentence'])
        return JsonResponse(data)

"""
    Class AllTop - view all top sentence
"""

class AllTop(ListView):
    template_name = 'sentences/alltopsentences.html'
    context_object_name = 'top_category_sent'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(AllTop, self).get_context_data(**kwargs)
        context['data_ctr'] = ModelHelpers.get_data_ctr()
        context['true_path'] = '/'.join(self.request.path.split('/')[0:2])
        return context

    def get_queryset(self):
        return Sentence.objects.get_all_top_sent()