import os
from datetime import datetime, timedelta

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

from mainbfg.models import (Categories, TypeSentence, Regions, SentenceForm, Image, Sentence)

"""
    Main page user office
"""


class PrivateOfficeView(LoginRequiredMixin, TemplateView):

    login_url = 'login'
    template_name = 'privateoffice.html'

    def get_context_data(self, **kwargs):
        context = super(PrivateOfficeView, self).get_context_data()
        context['active_tab'] = kwargs['tab'] if kwargs['tab'] else 'sent'
        try:
            context['active_sentences'] = Sentence.objects.only('id', 'caption', 'main_img', 'type_s', 'status', 'views', 'phone_views', 'create_time').\
                                                           filter(user_id=self.request.user.id).\
                                                           filter(status__in=[0, 1, 2])
            context['status_ss'] = {0:'На модерации', 1:'Опубликовано', 2:'На редактировании', 3:'Не активно'}
            context['type_ss'] = {0:'Обычное', 1:'TOP', 2:'VIP'}
        except Sentence.DoesNotExist:
            pass

        return context


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
    succes_url = '/user/privateoffice/'
    type_img_s = {1:'images/label-01-102x75.png', 2:'images/label-02-105x95.png',
                  3:'images/label-03-98-71.png'}

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.stop_time = datetime.now() + timedelta(days=30)
        instance.type_img_s = self.type_img_s[form.cleaned_data['type_id']]
        instance.identifier = self.uuid_sentece()
        instance.dirname_img = self.uuid_sentece_user()
        instance.link_name = self.slugify(form.cleaned_data['caption']) + '#' + instance.identifier
        instance.save()
        self.save_oter_files(instance, form)

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

    def uuid_sentece_user(self):
        import uuid
        return 'user_'+str(uuid.uuid4())[:10]

    def uuid_sentece(self):
        import uuid
        return str(uuid.uuid4())[:10]

    def save_oter_files(self, instance, form):
        if not os.path.isdir(settings.TEST_MEDIA_IMAGES+instance.dirname_img) and self.request.FILES.getlist('other_img[]'):
            os.mkdir(settings.TEST_MEDIA_IMAGES+instance.dirname_img, mode=0o777)
        #https://docs.djangoproject.com/ja/1.11/_modules/django/utils/datastructures/ - look for MultiValueDict(getlist)
        if self.request.FILES.getlist('other_img[]'):
            for ifile in self.request.FILES.getlist('other_img[]'):
                if ifile.size < settings.MAX_SIZE_UPLOAD and ifile.content_type in settings.CONTENT_TYPES_FILE:
                    fs = FileSystemStorage(location=settings.TEST_MEDIA_IMAGES+instance.dirname_img,
                                           base_url=settings.TEST_MEDIA_IMAGES+instance.dirname_img)
                    filename = fs.save(ifile.name, ifile)
                    i = Image(sentence=instance,
                              img_path=fs.url(filename))
                    i.save()
                else:
                    #messages.info(self.request, 'Three credits remain in your account.')
                    continue
        return True