from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

from mainbfg.mainhelpers import MainImgTypeField as MI
#------------------------- TypeSentence Model -----------------------------------------------#
"""
Custom Manadger for model TypeSentence
"""


class ManadgerTypeSentence(models.Manager):
#Get active Types
    def get_active_types(self):
        return self.get_queryset().filter(is_active__exact= True)


class TypeSentence(models.Model):
    name = models.CharField(max_length=50)
    link_name = models.CharField(max_length=50, default='')
    is_active = models.BooleanField(default=True)
    object = ManadgerTypeSentence()

    def get_absolute_url(self):
        return "/%s/" % self.link_name

    def __str__(self):
        return self.name

#----------------------------- Categories Model----------------------------------------------------
"""
Custom Manadger for model Categories
"""


class ManadgerCategories(models.Manager):
#Get active Categories
    def get_active_categories(self):
        return self.get_queryset().filter(is_active__exact = True)

#Get categories on 5 ps.
    def get_list_categories(self):
        activecategories = self.get_active_categories()
        return [activecategories[i:i+5] for i in range(0, len(activecategories), 5)]


class Categories(models.Model):
    name = models.CharField(max_length=50)
    link_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    icon_style = models.CharField(max_length=50, default='')
    is_icon_img = models.BooleanField(default=False)
    max_num = models.SmallIntegerField(default=1)
    paid_num = models.SmallIntegerField(default=5)
    object = ManadgerCategories()

    def get_absolute_url(self):
        return "/categories/%s/" % self.link_name

    def __str__(self):
        return self.name

#-------------------------------- Regions Model -------------------------------------------


class Regions(models.Model):
    name = models.CharField(max_length=100)
    link_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return "/%s/" % self.link_name

    def __str__(self):
        return self.name



#-------------------------------- Sentence Model -------------------------------------------#
# class ModelClass(models.Model):
#     <поле> = models.ImageField(upload_to=rename_image, blank=True, verbose_name='...')
#
# def rename_image(instance, filename):
#     image_name = md5(str(time.time()).encode()).hexdigest()
#     image_type = filename.split('.')[-1]
#     return 'imgs/{}.{}'.format(image_name, image_type)


def custom_directory_path(instance, filename):
    return 'images/{0}/{1}'.format(instance.dirname_img, filename)

class Sentence(models.Model):

    type_id = models.SmallIntegerField()
    category_id = models.SmallIntegerField()
    sub_id = models.SmallIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    autor = models.CharField(max_length=30, error_messages={'max_length' : 'Required error'})
    caption = models.CharField(max_length=50)
    region_id = models.SmallIntegerField()
    full_adress = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    web_site = models.CharField(max_length=250, blank=True)
    is_webstore = models.BooleanField(default=False)
    description = models.TextField(max_length=1000)
    meta_info = models.CharField(max_length=500, blank=True)
    main_img = MI.MainImgTypeField(upload_to=custom_directory_path,
                                   content_types=['image/jpeg', 'image/jpg', 'image/png', 'image/jpeg'],
                                   max_upload_size=5000000, blank=True, default='nophoto.png')
    dirname_img = models.CharField(max_length=15, default='', blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    stop_time = models.DateTimeField(blank=True)
    status = models.SmallIntegerField(default=0) #0 - on moderations, 1 - published, 2 - on editing
    type_s = models.SmallIntegerField(default=0) #0 - usual, 1 - TOP, 2 - VIP
    type_img_s = models.CharField(max_length=300, blank=True)#path to img (Stock, Discount, Sale)
    views = models.IntegerField(default=0)
    phone_views = models.IntegerField(default=0)
    text_message = models.CharField(max_length=1000, blank=True)
    is_paid = models.BooleanField(default=False)
    start_time_paid = models.DateTimeField(auto_now_add=True)
    end_time_paid = models.DateTimeField(auto_now_add=True)
    on_moderation = models.BooleanField(default=False)
    link_name = models.CharField(max_length=550)
    identifier = models.CharField(max_length=20)


    def get_absolute_url(self):
        return "sentence/%s" % self.link_name


    def __str__(self):
        return self.link_name


class SentenceForm(ModelForm):
    class Meta:
        model = Sentence
        fields = ['autor', 'caption', 'type_id', 'category_id', 'region_id', 'full_adress',
                  'phone', 'web_site', 'is_webstore', 'meta_info', 'description', 'main_img']

        error_messages = {
                             'autor': {'required': "Пожалуйста введите автора",
                                       'max_length':"Не более 30 символов"
                              },
                             'caption': {'required': "Пожалуйста введите заголовок",
                                         'max_length': "Не более 50 символов"
                              },
                             'description': {'required': "Пожалуйста введите описание",
                                             'max_length': "Не более 1000 символов"
                             },
                             'full_adress': {'max_length': "Не более 100 символов"},
                             'meta_info': {'max_length': "Не более 500 символов"},
                        }

#---------------------------------Images Model----------------------------------------------#

class Image(models.Model):

    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, related_name='image')
    img_path = models.CharField(max_length=250, blank=True)


    def get_absolute_url(self):
        return self.img_path

#-------------------------------- Payments Model -------------------------------------------#

class Payment(models.Model):
    pass


#----------------------------------Favorites Model ----------------------------------------#

class Favorite(models.Model):
    pass

#-------------------------------- Profile Model -------------------------------------------#

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

    #payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    #favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)


#-------------------------------- Subscription Model -------------------------------------------#

class Subscription(models.Model):
    pass

#-------------------------------- Subscriber Model -------------------------------------------#

class Subscriber(models.Model):
    pass

#-------------------------------SentenceMessage------------------------------------------------#

class SentensceMessage(models.Model):
    sentence_id = models.IntegerField()