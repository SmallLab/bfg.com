from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

from mainbfg.models import (Categories, TypeSentence, Regions, SentenceForm)


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
    form_class = SentenceForm
    template_name = 'addsentens.html'
    succes_url = '/'
    type_img_s = {1:'/static/images/label-01-102x75.png', 2:'/static/images/label-02-105x95.png',
                  3:'/static/images/label-03-98-71.png'}

    def form_valid(self, form):

        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.stop_time = datetime.now() + timedelta(days=30)
        instance.type_img_s = self.type_img_s[form.cleaned_data['type_id']]
        instance.identifier = self.uuid_sentece()
        instance.link_name = self.slugify(form.cleaned_data['caption']) + '#' + instance.identifier
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


    def slugify(swlf, str):
        import re
        import unidecode
        return re.sub(r'\s+', '-', unidecode.unidecode(str).lower().strip())

    def uuid_sentece(self):
        import uuid
        return str(uuid.uuid4())[:8]
