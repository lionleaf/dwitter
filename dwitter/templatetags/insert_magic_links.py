import re
from django import template

register = template.Library()


def user_dweet_to_link(m):
    text = m.group('text')
    dweet_id = m.group('dweet_id')
    username = m.group('username')

    if username is None:
        url = 'd/' + dweet_id
    else:
        url = 'u/' + username

    result = '<a href="/{0}">{0}</a>'.format(url)
    return text.replace(url, result)


def hashtag_to_link(m):
    text = m.group('text')
    hashtag = m.group('hashtag')

    url = 'h/' + hashtag
    tag = '#' + hashtag

    if not re.search('[a-zA-Z]', hashtag):
        return tag # hashtag contains no letters, return the plain tag
    
    result = '<a href="/{0}">{1}</a>'.format(url, tag)
    return text.replace(tag, result)


@register.filter(is_safe=True)
def insert_magic_links(text):
    text = re.sub(
        r'(?:^|(?<=\s))'                                       # start of string or whitespace
        r'/?'                                                  # optional /
        r'(?P<text>'                                           # capture original pattern
        r'[^a-zA-Z\d]?d/(?P<dweet_id>\d+)[^a-zA-Z]?'           # dweet reference
        r'|'                                                   # or
        r'[^a-zA-Z\d]?u/(?P<username>[\w.@+-]+)[^a-zA-Z\d]?)'  # user reference
        # end of string, whitespace or hashtag:
        r'(?=$|\s|#)',
        user_dweet_to_link,
        text
    )
    text = re.sub(
        # capture original pattern
        r'(?P<text>'
        # hashtag - check for whitespace precedence and word boundaries
        r'(?<!\S)#(?P<hashtag>[_a-zA-Z\d]+)\b)',
        hashtag_to_link,
        text
    )
    return text
