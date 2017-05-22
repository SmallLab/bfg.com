from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from mainbfg.models import (Categories, TypeSentence, Regions, Sentence)


"""
    Show form for add new sentense
"""

class ShowFormSentenseView(LoginRequiredMixin, TemplateView):

    login_url = 'login'
    template_name = 'addsentens.html'

    def get_context_data(self, **kwargs):
        context = super(ShowFormSentenseView, self).get_context_data(**kwargs)
        context['types'] = TypeSentence.object.get_active_types()
        context['categories'] = Categories.object.get_active_categories()
        context['regions'] = Regions.objects.all()
        return context


"""
    Create new sentence
"""

class CreateNewSentence(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Sentence
    fields = ['autor', 'caption', 'type_id', 'category_id', 'region_id', 'full_adress',
              'phone', 'web_site', 'is_webstore', 'meta_info', 'description']
    template_name = 'addsentens.html'
    succes_url = '/'

    def form_valid(self, form):

        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.stop_time = datetime.now() +  timedelta(days=30)
        instance.save()

        return super(CreateNewSentence, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['data'] = self.request.POST
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super(CreateNewSentence, self).get_context_data(**kwargs)
        context['types'] = TypeSentence.object.get_active_types()
        context['categories'] = Categories.object.get_active_categories()
        context['regions'] = Regions.objects.all()
        return context

    def get_success_url(self):
        return self.succes_url