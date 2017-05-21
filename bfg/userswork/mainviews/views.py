from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from mainbfg.models import Categories, TypeSentence, Regions


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
