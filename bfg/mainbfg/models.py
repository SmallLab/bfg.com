from django.db import models

"""
Model for type sentence
"""

class TypeSentence(models.Model):
    name = models.CharField(max_length=50)
    link_name = models.CharField(max_length=50, default='')
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return "/%s/" % self.link_name

    def __str__(self):
        return self.name


"""
    Model fo categories sentence
"""
class Categories(models.Model):
    name = models.CharField(max_length=50)
    link_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return "/%s/" % self.link_name

    def __str__(self):
        return self.name
