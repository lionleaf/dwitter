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

    result = '<a href="/{0}">{1}</a>'.format(url, tag)
    return text.replace(tag, result)


@register.filter(is_safe=True)
def insert_magic_links(text):
    text = re.sub(
        r'(?:^|(?<=\s))'                                        # start of string or whitespace
        r'/?'                                                   # optional /
        r'(?P<text>'                                            # capture original pattern
        r'[^a-zA-Z\d]?d/(?P<dweet_id>\d+)[^a-zA-Z]?'            # dweet reference
        r'|'                                                    # or
        r'[^a-zA-Z\d]?u/(?P<username>[\w.@+-]+)[^a-zA-Z\d]?)'   # user reference
        r'(?=$|\s|#)',                                       # end of string, whitespace or hashtag
        user_dweet_to_link,
        text
    )
    text = re.sub(
        r'(?P<text>'                                            # capture original pattern
        # (?:^|\s)    # go to the start of the line or the next space
        # (?=\S*#)    # lookahead to see is there a '#' after a bunch of non-whitespace characters?
        # (?!\S*:)    # lookahead to check aren't any ':' characters there (otherwise it's likely an anchor)
        # \S*#        # skip any of the characters leading up to the '#'
        # then do the hashtag grouping that was there before:
        # (?P<hashtag>[_a-zA-Z][_a-zA-Z\d]*)        
        r'(?:^|\s)(?=\S*#)(?!\S*:)\S*#(?P<hashtag>[_a-zA-Z][_a-zA-Z\d]*))',
        hashtag_to_link,
        text
    )
    return text
