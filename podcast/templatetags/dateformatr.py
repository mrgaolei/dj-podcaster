import time
from django import template

register = template.Library()

@register.filter
def dateformatr(value):
    return value.strftime("%a, %d %b %Y %X %z")

