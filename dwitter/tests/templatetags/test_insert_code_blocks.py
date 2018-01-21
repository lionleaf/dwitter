from django.test import TestCase
from dwitter.templatetags.insert_code_blocks import insert_code_blocks


class DweetTestCase(TestCase):
    def test_insert_code_blocks_wraps_stuff_inside_backticks(self):
        self.assertEqual(
            '<code>a</code>',
            insert_code_blocks('`a`')
        )

    def test_insert_code_blocks_ignores_backticks(self):
        self.assertEqual(
            '<code>a=`b`</code>',
            insert_code_blocks('`a=\`b\``')
        )

    def test_insert_code_blocks_is_not_greedy_with_multiple_blocks(self):
        self.assertEqual(
            'a <code>1</code> b <code>2</code> c',
            insert_code_blocks('a `1` b `2` c')
        )
