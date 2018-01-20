from django.test import TestCase
from dwitter.templatetags.insert_code_blocks import insert_code_blocks


class DweetTestCase(TestCase):
    def test_insert_code_blocks_wraps_stuff_inside_backticks(self):
        self.assertEqual(
            '<code>a</code>',
            insert_code_blocks('`a`')
        )

    def test_insert_code_blocks_ignored_backticks(self):
        self.assertEqual(
            '<code>a=`b`</code>',
            insert_code_blocks('`a=\`b\``')
        )
