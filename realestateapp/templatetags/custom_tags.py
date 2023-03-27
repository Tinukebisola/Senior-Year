# from django.template.defaulttags import register
from django import template
from django.template.defaultfilters import stringfilter
import requests
from django import template
import base64
register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_item_length(dictionary, key):
    return len(dictionary.get(key))

@register.filter
def get_item_length_perc(dictionary, key, total):
    return (len(dictionary.get(key))/total) * 100


@register.filter
def to_base64(url):
    return "data:image/png;base64, " + str(base64.b64encode(requests.get(url).content))

@register.filter
def length(x):
    return len(x)

@register.filter
def length_perc(x, total):
    return (len(x)/total) * 100


@register.filter
def get_item_capital(dictionary, key):
    return dictionary.get(key).capitalize()
