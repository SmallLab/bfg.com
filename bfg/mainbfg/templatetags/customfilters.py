from django import template

register = template.Library()

def strint(value, arg):
    return value[arg]

def strintlist(value, arg):
    try:
        return value[arg]
    except IndexError:
        return None

def strtoint(value):
    return int(value)

register.filter('strintlist', strintlist)
register.filter('strint', strint)
register.filter('strtoint', strtoint)