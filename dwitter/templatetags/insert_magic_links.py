import re
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


def to_link(m):
    text = m.group('text')
    dweet_id = m.group('dweet_id')
    username = m.group('username')

    if username is None:
        path = reverse('dweet_show', kwargs={'dweet_id': dweet_id})
    else:
        path = reverse('user_feed', kwargs={'url_username': username})

    return '<a href="%s">%s</a>' % (path, text)

@register.filter(is_safe=True)
def insert_magic_links(text):
    return re.sub(r'(?:^|(?<=\s))(?P<text>/d/(?P<dweet_id>\d+)|/u/(?P<username>[\w.@+-]+))(?=$|\s)', to_link, text)
