from datetime import datetime
from django.utils.timezone import now
from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.cache import cache

from mainbfg.mainhelpers import MainImgTypeField as MI

# ------------------------- TypeSentence Model -----------------------------------------------#
"""
Custom Manadger for model TypeSentence
"""


class ManagerTypeSentence(models.Manager):
  # Get single TypeCategory
  def get_single_type(self, link_name):
    return self.get_queryset().get(link_name=link_name)

  # Get active Types
  def get_active_types(self):
    return self.get_queryset().filter(is_active__exact=True)

  # Get dict {'link_name':{data object}, ...} for TypeSentence
  def get_dict_types(self):
    if cache.get('dictType'):
      return cache.get('dictType')
    else:
      new_dict = {'all': {'id': 0, 'link_name': 'all', 'name': 'Все'}}
      dictType = self.get_queryset().filter(is_active__exact=True).values()
      new_dict.update({a['link_name']: a for a in dictType})
      cache.set('dictType', new_dict)
      return new_dict


class TypeSentence(models.Model):
  name = models.CharField(max_length=50)
  link_name = models.CharField(max_length=50, default='')
  is_active = models.BooleanField(default=True)
  objects = ManagerTypeSentence()

  def get_absolute_url(self):
    return "/%s/" % self.link_name

  def __str__(self):
    return self.name


# ----------------------------- Categories Model----------------------------------------------------
"""
Custom Manadger for model Categories
"""


class ManagerCategories(models.Manager):
  # Get active Categories
  def get_active_categories(self):
    return self.get_queryset().filter(is_active__exact=True)

  # Get single Category
  def get_single_category(self, link_name):
    return self.get_queryset().get(link_name=link_name)

  # Get name Category
  def get_name_category(self, link_name):
    return self.get_queryset().only('name').get(link_name=link_name)

  # Get dict {'link_name':{data object}, ...} for Categories
  def get_dict_categories(self):
    if cache.get('dictCategory'):
      return cache.get('dictCategory')
    else:
      dictCategory = self.get_queryset().filter(is_active__exact=True).values()
      new_dict = {a['link_name']: a for a in dictCategory}
      cache.set('dictCategory', new_dict)
      return new_dict

  # Get categories on 5 ps.
  def get_list_categories(self):
    activecategories = self.get_active_categories()
    return [activecategories[i:i + 5] for i in range(0, len(activecategories), 5)]


class Categories(models.Model):
  name = models.CharField(max_length=50)
  link_name = models.CharField(max_length=50)
  is_active = models.BooleanField(default=True)
  icon_style = models.CharField(max_length=50, default='')
  is_icon_img = models.BooleanField(default=False)
  max_num = models.SmallIntegerField(default=1)
  paid_num = models.SmallIntegerField(default=5)
  objects = ManagerCategories()

  def get_absolute_url(self):
    return "/categories/%s/" % self.link_name

  def __str__(self):
    return self.name


# -------------------------------- Regions Model -------------------------------------------


class ManageRegions(models.Manager):

  def get_all_regions(self):
    return Regions.objects.all()

  def get_single_region_name(self, pk):
    return Regions.objects.only('name').get(pk=pk)


class Regions(models.Model):
  name = models.CharField(max_length=100)
  link_name = models.CharField(max_length=100)
  is_active = models.BooleanField(default=True)
  objects = ManageRegions()

  def get_absolute_url(self):
    return "/%s/" % self.link_name

  def __str__(self):
    return self.name


# -------------------------------- Sentence Model -------------------------------------------#
# class ModelClass(models.Model):
#     <поле> = models.ImageField(upload_to=rename_image, blank=True, verbose_name='...')
#
# def rename_image(instance, filename):
#     image_name = md5(str(time.time()).encode()).hexdigest()
#     image_type = filename.split('.')[-1]
#     return 'imgs/{}.{}'.format(image_name, image_type)


def custom_directory_path(instance, filename):
  return 'images/{0}/{1}'.format(instance.dirname_img, filename)


class ManagerSentences(models.Manager):
  """
    Work with site sentences
    """

  def get_sent_for_view(self):
    try:
      return Sentence.objects.filter(status=1).only('id', 'caption', 'type_img_s', 'autor', 'web_site')
    except Sentence.DoesNotExist:
      return False

  def get_all_top_sent(self):
    try:
      return Sentence.objects.filter(status=1).only('id', 'caption', 'type_img_s', 'autor', 'web_site')
    except Sentence.DoesNotExist:
      return False

  def get_filter_sentences(self, data):
    is_webstore = int(data.pop('is_webstore'))
    query = Sentence.objects
    work_dict = {}
    for param in data:
      if data[param]:
        work_dict[param] = data[param]
    if is_webstore == 1:
      work_dict['is_webstore'] = 1
    try:
      if is_webstore == 2:
        return query.filter(**work_dict).filter(status=1). \
          only('id', 'caption', 'type_img_s', 'autor', 'web_site'). \
          exclude(is_webstore=1).order_by('create_time')
      else:
        return query.filter(**work_dict).filter(status=1).only('id', 'caption', 'type_img_s',
                                                               'autor', 'web_site') \
          .order_by('create_time')
    except Sentence.DoesNotExist:
      return False

  def get_category_sentences(self, category_id, type_id=0):
    if type_id:
      return Sentence.objects.filter(category_id=category_id).filter(type_id=type_id).filter(status=1). \
        only('id', 'caption', 'type_img_s', 'autor', 'web_site').order_by('create_time')
    else:
      return Sentence.objects.filter(category_id=category_id).filter(status=1). \
        only('id', 'caption', 'type_img_s', 'autor', 'web_site'). \
        order_by('create_time')

  def get_top_sentences_start_page(self):
    """
           later add filter(type_s=1) for TOP sent
        """
    index = 0
    try:
      all_top = Sentence.objects.filter(status=1)[index:index + 12].only('id', 'caption', 'type_img_s',
                                                                         'autor', 'web_site')
      top_sentences = [all_top[i:i + 4] for i in range(0, len(all_top), 4)]
      return top_sentences
    except Sentence.DoesNotExist:
      return False

  def get_top_sentences_category_page(self, category_id, type_id=0):
    """
        later add filter(type_s=1) for TOP sent
        """
    count = 5
    try:
      import random
      if type_id:
        index = random.randint(1, Sentence.objects.filter(status=1).filter(category_id=category_id).
                               filter(type_id=type_id).count())
        return Sentence.objects.filter(status=1).filter(category_id=category_id).filter(type_id=type_id)[
               index:index + count]. \
          only('id', 'caption', 'type_img_s', 'autor', 'web_site')
      else:
        index = random.randint(1, Sentence.objects.filter(status=1).filter(category_id=category_id).count())
        return Sentence.objects.filter(status=1).filter(category_id=category_id)[index:index + count]. \
          only('id', 'caption', 'type_img_s', 'autor', 'web_site')
    except (Sentence.DoesNotExist, ValueError):
      return False

  def get_top_sent_filter_page(self, data):
    count = 5
    is_webstore = int(data.pop('is_webstore'))
    query = Sentence.objects
    work_dict = {}
    for param in data:
      if data[param]:
        work_dict[param] = data[param]
    if is_webstore == 1:
      work_dict['is_webstore'] = 1
    try:
      if is_webstore == 2:
        import random
        index = random.randint(1, Sentence.objects.filter(status=1).filter(**work_dict).exclude(is_webstore=1).count())
        return query.filter(**work_dict).exclude(is_webstore=1)[index:index + count]. \
          only('id', 'caption', 'type_img_s', 'autor', 'web_site')
      else:
        import random
        index = random.randint(1, Sentence.objects.filter(status=1).filter(**work_dict).count())
        return query.filter(**work_dict)[index:index + count]. \
          only('id', 'caption', 'type_img_s', 'autor', 'web_site')
    except (Sentence.DoesNotExist, ValueError):
      return False

  def get_phone(self, pk):
    obj = Sentence.objects.only('phone').get(pk=pk)
    if obj.phone:
      obj.phone_views += 1
      obj.save()
      return {'status': True, 'phone': obj.phone}
    else:
      return {'status': False}

  """
    Work with users office sentences
    """

  def get_active_sentences(self, user_id, status_list=[0, 1, 2]):
    try:
      return Sentence.objects.only('id', 'caption', 'main_img', 'type_s', 'status', 'views', 'phone_views',
                                   'create_time'). \
        filter(user_id=user_id). \
        filter(status__in=status_list)
    except Sentence.DoesNotExist:
      return False

  def get_deactive_sentences(self, user_id, status=3):
    try:
      return Sentence.objects.only('id', 'caption', 'main_img', 'type_s', 'status',
                                   'views', 'phone_views', 'create_time'). \
        filter(user_id=user_id). \
        filter(status=status)
    except Sentence.DoesNotExist:
      return False

  def get_single_sentence(self, pk):
    try:
      return Sentence.objects.get(pk=pk)
    except Sentence.DoesNotExist:
      return False

  def deactive_sentence(self, pk):
    edit_data = Sentence.objects.get(pk=pk)
    edit_data.status = 3
    edit_data.save()
    return None

  def active_sentence(self, pk):
    edit_data = Sentence.objects.get(pk=pk)
    edit_data.status = False
    edit_data.on_moderation = False
    edit_data.save()
    return None


class Sentence(models.Model):
  type_id = models.SmallIntegerField()
  category_id = models.SmallIntegerField()
  sub_id = models.SmallIntegerField(default=0)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sentences')
  autor = models.CharField(max_length=30, error_messages={'max_length': 'Required error'}, default='', blank=True)
  caption = models.CharField(max_length=50)
  region_id = models.SmallIntegerField()
  full_adress = models.CharField(max_length=100, blank=True)
  phone = models.CharField(max_length=100, blank=True)
  web_site = models.CharField(max_length=250, blank=True)
  is_webstore = models.BooleanField(default=False)
  description = models.TextField(max_length=1000)
  meta_info = models.CharField(max_length=500, blank=True)
  main_img = MI.MainImgTypeField(upload_to=custom_directory_path, content_types=['image/jpg', 'image/png', 'image/jpeg'],
                                   max_upload_size=5000000,
                                  blank=True, default='nophoto.png')
  dirname_img = models.CharField(max_length=15, default='', blank=True)
  create_time = models.DateTimeField(auto_now_add=True)
  stop_time = models.DateTimeField(blank=True)
  status = models.SmallIntegerField(default=0)  # 0 - on moderations, 1 - published, 2 - on editing, 3- deactive
  type_s = models.SmallIntegerField(default=0)  # 0 - usual, 1 - TOP, 2 - VIP
  type_img_s = models.CharField(max_length=300, blank=True)  # path to img (Stock, Discount, Sale)
  views = models.IntegerField(default=0)
  phone_views = models.IntegerField(default=0)
  text_message = models.CharField(max_length=65, blank=True)
  is_send_mess = models.BooleanField(default=False)
  is_paid = models.BooleanField(default=False)
  start_time_paid = models.DateTimeField(auto_now_add=True)
  end_time_paid = models.DateTimeField(auto_now_add=True)
  on_moderation = models.BooleanField(default=False)
  link_name = models.CharField(max_length=550)
  identifier = models.CharField(max_length=20)
  price = models.IntegerField(default=0, blank=True)
  objects = ManagerSentences()

  # change the main_imgfield value to be the newley modifed image value - png
  def save(self, update_fields=None):
    super(Sentence, self).save()
    from PIL import Image
    from io import BytesIO
    from django.core.files.uploadedfile import InMemoryUploadedFile
    import sys
    # Opening the uploaded image
    im = Image.open(self.main_img)
    output = BytesIO()
    # Resize/modify the image
    im = im.resize((277, 205))
    # after modifications, save it to the output
    im.save(output, format='PNG', quality=100)
    output.seek(0)
    # change the main_imgfield value to be the newley modifed image value - png
    self.main_img = InMemoryUploadedFile(output, 'MI.MainImgTypeField', "%s.png" % self.main_img.name.split('.')[0],
                                         'image/png',
                                         sys.getsizeof(output), None)

  def get_region(self):
    return Regions.objects.get_single_region_name(self.region_id)

  def get_absolute_url(self):
    return "sentence/%s" % self.link_name

  def __str__(self):
    return self.link_name


class SentenceForm(ModelForm):
  class Meta:
    model = Sentence
    fields = ['autor', 'caption', 'type_id', 'category_id', 'region_id', 'full_adress',
              'phone', 'web_site', 'is_webstore', 'meta_info', 'description', 'main_img', 'price', 'text_message']

    error_messages = {
      'autor': {'required': "Пожалуйста введите автора!!!",
                'max_length': "Не более 30 символов"
                },
      'caption': {'required': "Пожалуйста введите заголовок!!!",
                  'max_length': "Не более 50 символов"
                  },
      'description': {'required': "Пожалуйста введите описание!!!",
                      'max_length': "Не более 1000 символов"
                      },
      'full_adress': {'max_length': "Не более 100 символов"},
      'meta_info': {'max_length': "Не более 500 символов"},
      'price': {'max_length': "Не более 5 символов"},
      'text_message': {'max_length': "Не более 65 символов"},
    }


class SentenceEditForm(ModelForm):
  class Meta:
    model = Sentence
    fields = ['autor', 'caption', 'type_id', 'category_id', 'region_id', 'full_adress',
              'phone', 'web_site', 'is_webstore', 'meta_info', 'description', 'main_img', 'price', 'text_message']

    error_messages = {
      'autor': {'required': "Пожалуйста введите автора!!!",
                'max_length': "Не более 30 символов"
                },
      'caption': {'required': "Пожалуйста введите заголовок!!!",
                  'max_length': "Не более 50 символов"
                  },
      'description': {'required': "Пожалуйста введите описание!!!",
                      'max_length': "Не более 1000 символов"
                      },
      'full_adress': {'max_length': "Не более 100 символов"},
      'meta_info': {'max_length': "Не более 500 символов"},
      'price': {'max_length': "Не более 5 символов"},
      'text_message': {'max_length': "Не более 65 символов"},
    }


# ---------------------------------Images Model----------------------------------------------#


class Image(models.Model):
  sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, related_name='image')
  img_path = models.CharField(max_length=250, blank=True)

  def get_absolute_url(self):
    return self.img_path


# -------------------------------- Payments Model -------------------------------------------#


class Payment(models.Model):
  pass


# ----------------------------------Favorites Model ----------------------------------------#


class Favorite(models.Model):
  pass


# -------------------------------- Profile Model -------------------------------------------#
class ManageProfile(models.Manager):

  def set_autor_field(self, profile, autor):
    if profile.autor:
      return False
    else:
      profile.autor = autor
      profile.save()
      return True


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  phone = models.CharField(blank=True, max_length=100)
  email = models.EmailField(blank=True, max_length=255)
  favorite_num = models.SmallIntegerField(blank=True, default=0)
  is_subscrabtion = models.BooleanField(default=False)
  is_subscriber = models.BooleanField(default=False)
  facebook_id = models.BigIntegerField(blank=True, default=0)
  vk_id = models.IntegerField(blank=True, default=0)
  first_name = models.CharField(max_length=50, blank=True)
  last_name = models.CharField(max_length=50, blank=True)
  autor = models.CharField(max_length=100, blank=True, default='')
  objects = ManageProfile()

  # payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
  # favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)


# -------------------------------- Subscription Model -------------------------------------------#
class ManageSubscription(models.Manager):

  def addsubscription(self, user, sub_user_id, type_sub, data_send, autor):
    try:
      self.create(user=user, sub_user_id=sub_user_id, type_sub=type_sub, data_send=data_send, autor=autor)
      if type_sub == 0 and not user.profile.phone:
        user.profile.phone = data_send
        user.profile.save()
      elif type_sub == 1 and not user.profile.email:
        user.profile.email = data_send
        user.profile.save()
      return True
    except IntegrityError:
      return False

  def getcountsub(self, sub_user_id):
    return Subscription.objects.filter(sub_user_id=sub_user_id).count()

  def getuserlist(self, user_id):
    try:
      return Subscription.objects.only('sub_user_id')
    except Subscription.DoesNotExist:
      return False

  def deletesub(self, sub_id):
    Subscription.objects.filter(id=sub_id).delete()

  def change_active_status(self, pk):
    se = Subscription.objects.get(pk=pk)
    if se.is_active:
      se.is_active = False
      se.time_create_sub = datetime.now()
      data = {"status": False}
    else:
      se.is_active = True
      se.time_create_sub = datetime.now()
      data = {"status": True}
    se.save()
    return data


class Subscription(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription', default='')
  sub_user_id = models.IntegerField(default=0)
  type_sub = models.SmallIntegerField(default=0)  # type subscriptions - SMS - 0, Email - 1
  time_create_sub = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)
  data_send = models.CharField(max_length=100, default='')  # Phone number or email
  autor = models.CharField(max_length=100, default='')
  objects = ManageSubscription()


# -------------------------------SentenceMessage------------------------------------------------#


class SentensceMessage(models.Model):
  sentence_id = models.IntegerField()
