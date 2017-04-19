from django.db import models

############################### TypeSentence Model ################################
"""
Custom Manadger for model TypeSentence
"""
class ManadgerTypeSentence(models.Manager):
#Get active Types
    def get_active_types(self):
        return self.get_queryset().filter(is_active__exact= True)

"""
Model for type sentence
"""
class TypeSentence(models.Model):
    name = models.CharField(max_length=50)
    link_name = models.CharField(max_length=50, default='')
    is_active = models.BooleanField(default=True)
    object = ManadgerTypeSentence()

    def get_absolute_url(self):
        return "/%s/" % self.link_name

    def __str__(self):
        return self.name

########################## Categories Model#####################################
"""
Custom Manadger for model Categories
"""
class ManadgerCategories(models.Manager):
#Get active Categories
    def get_active_categories(self):
        return self.get_queryset().filter(is_active__exact = True)

"""
    Model fo categories sentence
"""
class Categories(models.Model):
    name = models.CharField(max_length=50)
    link_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    object = ManadgerCategories()

    def get_absolute_url(self):
        return "/categories/%s/" % self.link_name

    def __str__(self):
        return self.name

################################# Regions Model ##################################

class Regions(models.Model):
    name = models.CharField(max_length=100)
    link_name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/%s/" % self.link_name

    def __str__(self):
        return self.name