from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

"""
    Show form for add new sentense
"""

class AddNewSentenseView(LoginRequiredMixin, TemplateView):

    login_url = 'login'
    template_name = 'addsentens.html'
