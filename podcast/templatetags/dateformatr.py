import time
from django import template

register = template.Library()

@register.filter
def dateformatr(value):
    return value.strftime("%a, %d %b %Y %X %z")

@register.filter
def duration(value):
	h = value / 3600
	sec = value % 3600
	m = sec / 60
	s = sec % 60
	return "%d:%02d:%02d" % (h,m,s)