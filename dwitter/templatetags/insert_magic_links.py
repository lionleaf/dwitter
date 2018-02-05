import re
from django import template

register = template.Library()


def to_link(m):
    text = m.group('text')
    dweet_id = m.group('dweet_id')
    username = m.group('username')

    if username is None:
        url = 'd/' + dweet_id
    else:
        url = 'u/' + username

    result = '<a href="/{0}">{0}</a>'.format(url)
    return text.replace(url, result)


@register.filter(is_safe=True)
def insert_magic_links(text):
    return re.sub(
        r'(?:^|(?<=\s))'                                        # start of string or whitespace
        r'/?'                                                   # optional /
        r'(?P<text>'                                            # capture original pattern
        r'[^a-zA-Z\d]?d/(?P<dweet_id>\d+)[^a-zA-Z]?'            # dweet reference
        r'|'                                                    # or
        r'[^a-zA-Z\d]?u/(?P<username>[\w.@+-]+)[^a-zA-Z\d]?)'   # user reference
        r'(?=$|\s)',                                            # end of string or whitespace
        to_link,
        text
    )
