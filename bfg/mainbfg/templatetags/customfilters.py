from django import template

register = template.Library()

def strint(value):
    return 1

register.filter('strint', strint)