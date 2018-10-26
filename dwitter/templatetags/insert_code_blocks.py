import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def to_code_block(m):
    code = m.group('code')
    code = re.sub(r'\\`', '`', code)

    # remove anchors from code blocks
    a = re.findall(r'(<a[^<]*>(?P<link>[^<]*)</a>)', code)
    for i in range(len(a)):
        code = code.replace(a[i][0], a[i][1])

    return '<code>%s</code>' % code

@register.filter
def insert_code_blocks(text):
    result = re.sub(
        r'`'                # start with `
        r'(?P<code>.*?)'    # capture code block
        r'(?<!\\)'          # not preceded by \
        r'`',               # end with `
        to_code_block,
        text
    )
    return mark_safe(result)
