from django.db import models

###############################Model TypeSentence#######################################
"""
Custom Manadger for model TypeSentence
"""
class ManadgerTypeSentence(models.Manager):
#Get active Types
    def get_active_types(self):
        return self.get_queryset().filter(is_active = True)

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

##########################Model Categories#####################################
"""
Custom Manadger for model Categories
"""
class ManadgerCategories(models.Manager):
#Get active Categories
    def get_active_categories(self):
        return self.get_queryset().filter(is_active = True)

"""
    Model fo categories sentence
"""
class Categories(models.Model):
    name = models.CharField(max_length=50)
    link_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    object = ManadgerCategories()

    def get_absolute_url(self):
        return "/%s/" % self.link_name

    def __str__(self):
        return self.name
