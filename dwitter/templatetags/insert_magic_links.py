import re
from django import template

register = template.Library()


# find all long d/ and u/ links in http:// form through regex, and
# use replace() to singularly shorten each match into the d/ or u/ form
def autocrop_urls(m):
    d_links = re.findall(r'(?<!\S)((http(s|):\/\/|)(www\.|)dwitter\.net\/(d\/\d+))\b', m)
    u_links = re.findall(r'(?<!\S)((http(s|):\/\/|)(www\.|)dwitter\.net\/(u\/\S+))\b', m)
    for i in range(len(d_links)):
        if d_links:
            m = m.replace(d_links[i][0], d_links[i][4])
    for i in range(len(u_links)):
        if u_links:
            m = m.replace(u_links[i][0], u_links[i][4])
    return m


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
        return tag  # hashtag contains no letters, return the plain tag

    result = '<a href="/{0}">{1}</a>'.format(url, tag)
    return text.replace(tag, result)


@register.filter(is_safe=True)
def insert_magic_links(text):
    text = autocrop_urls(text)
    text = re.sub(
        # start of string or whitespace
        r'(?:^|(?<=\s))'
        # optional /
        r'/?'
        # capture original pattern
        r'(?P<text>'
        # dweet reference
        r'[^a-zA-Z\d]?d/(?P<dweet_id>\d+)(\s|\:|\;|\,|\!|\?|\.|\Z)?'
        # or
        r'|'
        # user reference
        r'(?<!\S)u\/(?P<username>[\w.@+-]+)(\s|\:|\;|\,|\!|\?|\.|\Z))'
        # end of string, whitespace or hashtag:
        r'(?=$|\s|#)',
        user_dweet_to_link,
        text
    )
    text = re.sub(
        # capture original pattern
        r'(?P<text>'
        # hashtag - check for whitespace precedence and word boundaries
        r'(?<!\S)#(?P<hashtag>[_a-zA-Z\d]+)(\s|\:|\;|\,|\!|\?|\.|\Z))',
        hashtag_to_link,
        text
    )
    return text
