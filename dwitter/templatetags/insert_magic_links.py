import re
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


def to_link(match):
    dweet_id = match.group(1)
    username = match.group(2)

    if username is None:
        path = reverse('dweet_show', kwargs={'dweet_id': dweet_id})
    else:
        path = reverse('user_feed', kwargs={'url_username': username})

    return '<a href="%s">%s</a>' % (path, match.group(0))

@register.filter(is_safe=True)
def insert_magic_links(text):
    return re.sub(r'/d/(\d+)|/u/([\w.@+-]+)', to_link, text)
