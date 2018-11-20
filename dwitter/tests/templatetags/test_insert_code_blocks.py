from django.test import TestCase
from dwitter.templatetags.insert_code_blocks import insert_code_blocks


class DweetTestCase(TestCase):
    
    def test_insert_code_wraps_stuff_inside_backticks(self):
        self.assertEqual(
            '<code>a</code>',
            insert_code_blocks('`a`')
        )


    def test_insert_code_ignores_backticks(self):
        self.assertEqual(
            '<code>a=`b`</code>',
            insert_code_blocks('`a=\`b\``')
        )


    def test_insert_code_is_not_greedy_with_multiple_blocks(self):
        self.assertEqual(
            'a <code>1</code> b <code>2</code> c',
            insert_code_blocks('a `1` b `2` c')
        )
        
    def test_insert_code_removes_anchors(self):
        self.assertEqual(
            'My sneaky link here, and also here.',
            insert_code_blocks('My sneaky <a href="link">link</a> here, and also <a href="link2">here</a>.')
        )
        
    def test_insert_code_with_no_code(self):
        try:
            insert_code_blocks('')
            insert_code_blocks('No code here, move along!')
        except:
            self.fail()
