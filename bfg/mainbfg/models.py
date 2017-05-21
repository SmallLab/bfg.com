from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class Sentence(models.Model):

    type_id = models.SmallIntegerField()
    category_id = models.SmallIntegerField()
    sub_id = models.SmallIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    autor = models.CharField(max_length=100)
    caption = models.CharField(max_length=200)
    region_id = models.SmallIntegerField()
    full_adress = models.CharField(max_length=350, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    web_site = models.CharField(max_length=250, blank=True)
    is_webstore = models.BooleanField(default=False)
    description = models.TextField()
    meta_info = models.CharField(max_length=1000, blank=True)
    main_img = models.ImageField(upload_to='images/', blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    stop_time = models.DateTimeField(blank=True)
    status = models.SmallIntegerField(default=0) #0 - on moderations, 1 - published, 2 - on editing
    type_s = models.SmallIntegerField(default=0) #0 - usual, 1 - TOP, 2 - VIP
    type_img_s = models.CharField(max_length=300)#path to img (Stock, Discount, Sale)
    views = models.IntegerField(default=0)
    phone_views = models.IntegerField(default=0)
    text_message = models.CharField(max_length=1000, blank=True)
    is_paid = models.BooleanField(default=False)
    start_time_paid = models.DateTimeField(blank=True)
    end_time_paid = models.DateTimeField(blank=True)
    on_moderation = models.BooleanField(default=False)
    link_name = models.CharField(max_length=550)
    identifier = models.CharField(max_length=20)


    def get_absolute_url(self):
        return "sentence/%s/%s/" % self.link_name, self.identifier


    def __str__(self):
        return self.link_name


#---------------------------------Images Model----------------------------------------------#

class ImagesSentences(models.Model):

    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    img_path = models.CharField(max_length=250 ,blank=True)



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