import hashlib
from django import template

register = template.Library()


@register.filter
def to_gravatar_url(email):
    return ('https://gravatar.com/avatar/%s?d=retro' %
            hashlib.md5((email or '').strip().lower().encode('utf-8')).hexdigest())
