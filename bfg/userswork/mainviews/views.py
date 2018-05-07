import os
import shutil
from datetime import datetime, timedelta

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView, RedirectView
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from userswork.mainhelpers import modelshelper
from mainbfg.models import (SentenceForm, Image, Sentence, SentenceEditForm, Profile, Subscription)

"""
    Main page user office
"""

class PrivateOfficeView(LoginRequiredMixin, TemplateView):

    login_url = 'login'
    template_name = 'privateoffice.html'

    def get_context_data(self, **kwargs):
        context = super(PrivateOfficeView, self).get_context_data()
        context['active_tab'] = kwargs['tab'] if kwargs['tab'] else 'sent'
        context['active_sentences'] = Sentence.objects.get_active_sentences(self.request.user.id)
        context['status_ss'] = {0:'На модерации', 1:'Опубликовано', 2:'На редактировании', 3:'Не активно'}
        context['type_ss'] = {0:'Обычное', 1:'TOP', 2:'VIP'}
        context['deactive_sentences'] = Sentence.objects.get_deactive_sentences(self.request.user.id)

        return context

"""
    Delete sentence
"""

class PODeleteSentenceView(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        del_sent_data = Sentence.objects.get_single_sentence(kwargs['pk'])
        shutil.rmtree(settings.TEST_MEDIA_IMAGES + del_sent_data.dirname_img, ignore_errors=True)
        del_sent_data.delete()

        return super(PODeleteSentenceView, self).get(self, request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('privateoffice', kwargs={'tab': 'sent'})

"""
    Deactivate sentence
"""

class PODeactiveSentenceView(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        Sentence.objects.deactive_sentence(kwargs['pk'])
        return super(PODeactiveSentenceView, self).get(self, request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('privateoffice', kwargs={'tab': 'sent'})

"""
    Activate sentence
"""

class POActiveSentenceView(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        Sentence.objects.active_sentence(kwargs['pk'])
        return super(POActiveSentenceView, self).get(self, request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('privateoffice', kwargs={'tab': 'sent'})

"""
    Edit sentence
"""

class POEditSentenceView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Sentence
    form_class = SentenceEditForm
    context_object_name = 'data'
    template_name = 'editsent.html'
    success_url = '/user/privateoffice/'
    type_img_s = {1: 'images/label-01-102x75.png', 2: 'images/label-02-105x95.png',
                  3: 'images/label-03-98-71.png'}

    def get_context_data(self, **kwargs):
        context = super(POEditSentenceView, self).get_context_data(**kwargs)
        context['types'], context['categories'], context['regions'] = modelshelper.get_tcr_data()
        context['range_img'] = range(7)
        context['action'] = reverse('editsent',
                                    kwargs={'pk': self.get_object().id})

        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.type_img_s = self.type_img_s[form.cleaned_data['type_id']]
        instance.link_name = self.slugify(form.cleaned_data['caption']) + '_' + instance.identifier
        # delete main file photo
        if int(self.request.POST['is_del_mainphoto']) == 0:
            instance.main_img.delete()
            instance.main_img = 'nophoto.png'
        if int(self.request.POST['is_del_other_photo']) == 1:
            self.delete_related_photo(instance, self.request.POST['list_del_other_photo'])
        instance.on_moderation = False
        instance.status = False
        instance.save()
        self.save_oter_files(instance, form)

        return super(POEditSentenceView, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        #context['data'] = self.request.POST
        context['action'] = reverse('editsent',
                                    kwargs={'pk': self.get_object().id})

        return self.render_to_response(context)

    def get_success_url(self):
        return self.success_url


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

    def delete_related_photo(self, instance, file_list):
        import json
        data = json.loads(file_list)
        for imaje in data:
            img = Image.objects.filter(id=imaje).get()
            try:
                os.remove(settings.BASE_DIR +'/'+ img.img_path)
                img.delete()
            except OSError:
               pass

"""
    Create new sentence
"""

class CreateNewSentence(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = SentenceForm
    template_name = 'addsentens.html'
    success_url = '/user/privateoffice/'
    type_img_s = {1:'images/label-01-102x75.png', 2:'images/label-02-105x95.png',
                  3:'images/label-03-98-71.png'}

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.stop_time = datetime.now() + timedelta(days=30)
        instance.type_img_s = self.type_img_s[form.cleaned_data['type_id']]
        instance.identifier = self.uuid_sentece()
        instance.dirname_img = self.uuid_sentece_user()
        instance.link_name = self.slugify(form.cleaned_data['caption']) + '_' + instance.identifier
        instance.save()
        self.save_oter_files(instance, form)
        Profile.objects.set_autor_field(self.request.user.profile, form.cleaned_data['autor'])
        return super(CreateNewSentence, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['data'] = self.request.POST

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(CreateNewSentence, self).get_context_data(**kwargs)
        context['types'], context['categories'], context['regions'] = modelshelper.get_tcr_data()
        return context

    def get_success_url(self):
        return self.success_url

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

"""
   Subscription work
"""

class DeleteSub(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        Subscription.objects.deleteSub(kwargs['pk'])

        return super(DeleteSub, self).get(self, request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('privateoffice', kwargs={'tab': 'subscribers'})

class DeactiveActiveSub(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = Subscription.objects.change_active_status(kwargs['pk'])
            return JsonResponse(data)
        else:
            return JsonResponse({'status':False})

class GetModalLogin(View):
    pass