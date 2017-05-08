from django.db import models
from django.contrib.auth.models import User

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
        activecategories = self.get_queryset().filter(is_active__exact = True)
        return [activecategories[i:i+5] for i in range(0, len(activecategories), 5)]


class Categories(models.Model):
    name = models.CharField(max_length=50)
    link_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    icon_style = models.CharField(max_length=50, default='')
    is_icon_img = models.BooleanField(default=False)
    object = ManadgerCategories()

    def get_absolute_url(self):
        return "/categories/%s/" % self.link_name

    def __str__(self):
        return self.name

#-------------------------------- Regions Model -------------------------------------------


class Regions(models.Model):
    name = models.CharField(max_length=100)
    link_name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/%s/" % self.link_name

    def __str__(self):
        return self.name



#-------------------------------- Sentence Model -------------------------------------------#

# class Sentence(models.Model):
#
#     type_id = models.SmallIntegerField()
#     category_id = models.SmallIntegerField()
#     sub_id = models.SmallIntegerField(default=0)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     autor = models.CharField(max_length=100)
#     caption = models.CharField(max_length=200)
#     region_id = models.SmallIntegerField()
#     full_adress = models.CharField(max_length=250, blank=True)
#     phone = models.CharField(max_length=100, blank=True)
#     web = models.CharField(max_length=250, blank=True)
#     is_webstore = models.BooleanField(default=False)
#     description = models.TextField()
#     main_img = models.CharField(max_length=250, blank=True)
#     create_time = models.DateTimeField(auto_now_add=True)
#     stop_time = models.DateTimeField(blank=True)
#     status = models.SmallIntegerField(default=0)
#     type_s = models.SmallIntegerField(default=0)
#     type_img_s = models.CharField(max_length=300)
#     meta_info = models.CharField(max_length=1000, blank=True)
#     views = models.IntegerField(default=0)
#     phone_views = models.IntegerField(default=0)
#     text_message = models.CharField(max_length=1000, blank=True)
#     is_paid = models.BooleanField(default=False)
#     start_time_paid = models.DateTimeField(blank=True)
#     end_time_paid = models.DateTimeField(blank=True)
#     on_moderation = models.BooleanField(default=False)


#-------------------------------- Payments Model -------------------------------------------#

class Payment(models.Model):
    pass


#-------------------------------- Profile Model -------------------------------------------#

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=100)
    email = models.EmailField(blank=True, max_length=255)
    favorite_num = models.SmallIntegerField(blank=True, default=0)
    count_sentence = models.SmallIntegerField(blank=True, default=0)
    is_subscrabtion = models.BooleanField(default=False)
    is_subscriber = models.BooleanField(default=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)