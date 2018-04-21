from django.test import TestCase
from dwitter.templatetags.insert_magic_links import insert_magic_links


class DweetTestCase(TestCase):
    def test_insert_magic_links_bypasses_html(self):
        self.assertEqual(
            'prefix <h1>content</h1> suffix',
            insert_magic_links('prefix <h1>content</h1> suffix')
        )

    # user

    def test_insert_magic_links_replaces_user_with_valid_characters(self):
        self.assertEqual(
            '<a href="/u/a1_.@+-">u/a1_.@+-</a>',
            insert_magic_links('u/a1_.@+-')
        )

    def test_insert_magic_links_bypasses_user_with_invalid_characters(self):
        self.assertEqual(
            'u/a1$',
            'u/a1$'
        )

    def test_insert_magic_links_replaces_standalone_user(self):
        self.assertEqual(
            '<a href="/u/a">u/a</a>',
            insert_magic_links('u/a')
        )

    def test_insert_magic_links_replaces_user_at_start_of_string(self):
        self.assertEqual(
            '<a href="/u/a">u/a</a> suffix',
            insert_magic_links('u/a suffix')
        )

    def test_insert_magic_links_replaces_user_at_end_of_string(self):
        self.assertEqual(
            'prefix <a href="/u/a">u/a</a>',
            insert_magic_links('prefix u/a')
        )

    def test_insert_magic_links_replaces_user_at_middle_of_string(self):
        self.assertEqual(
            'prefix <a href="/u/a">u/a</a> suffix',
            insert_magic_links('prefix u/a suffix')
        )

    def test_insert_magic_links_bypasses_user_prefixed_by_non_space(self):
        self.assertEqual(
            'prefixu/a suffix',
            insert_magic_links('prefixu/a suffix')
        )

    def test_insert_magic_links_bypasses_user_suffixed_by_non_space(self):
        self.assertEqual(
            'prefix u/a/suffix',
            insert_magic_links('prefix u/a/suffix')
        )

    def test_insert_magic_links_replaces_user_suffixed_by_slash(self):
        self.assertEqual(
            'prefix <a href="/u/a">u/a</a> prefix/u/a',
            insert_magic_links('prefix /u/a prefix/u/a')
        )

    def test_insert_magic_links_replaces_user_inside_parenthases(self):
        self.assertEqual(
            '(<a href="/u/a">u/a</a>)',
            insert_magic_links('(u/a)')
        )

    # dweet

    def test_insert_magic_links_replaces_dweet_with_valid_characters(self):
        self.assertEqual(
            '<a href="/d/1234567890">d/1234567890</a>',
            insert_magic_links('d/1234567890')
        )

    def test_insert_magic_links_bypasses_dweet_with_invalid_characters(self):
        self.assertEqual(
            'd/1a',
            'd/1a'
        )

    def test_insert_magic_links_replaces_standalone_dweet(self):
        self.assertEqual(
            '<a href="/d/1">d/1</a>',
            insert_magic_links('d/1')
        )

    def test_insert_magic_links_replaces_dweet_at_start_of_string(self):
        self.assertEqual(
            '<a href="/d/1">d/1</a> suffix',
            insert_magic_links('d/1 suffix')
        )

    def test_insert_magic_links_replaces_dweet_at_end_of_string(self):
        self.assertEqual(
            'prefix <a href="/d/1">d/1</a>',
            insert_magic_links('prefix d/1')
        )

    def test_insert_magic_links_replaces_dweet_at_middle_of_string(self):
        self.assertEqual(
            'prefix <a href="/d/1">d/1</a> suffix',
            insert_magic_links('prefix d/1 suffix')
        )

    def test_insert_magic_links_bypasses_dweet_prefixed_by_non_space(self):
        self.assertEqual(
            'prefixd/1 suffix',
            insert_magic_links('prefixd/1 suffix')
        )

    def test_insert_magic_links_bypasses_dweet_suffixed_by_non_space(self):
        self.assertEqual(
            'prefix d/1/suffix',
            insert_magic_links('prefix d/1/suffix')
        )

    def test_insert_magic_links_replaces_dweet_suffixed_by_slash(self):
        self.assertEqual(
            'prefix <a href="/d/1">d/1</a> prefix/d/1',
            insert_magic_links('prefix /d/1 prefix/d/1')
        )

    def test_insert_magic_links_replaces_dweet_in_parenthases(self):
        self.assertEqual(
            '(<a href="/d/1">d/1</a>)',
            insert_magic_links('(d/1)')
        )

    def test_insert_magic_replaces_basic_hashtag(self):
        self.assertEqual(
            '<a href="/h/test">#test</a>',
            insert_magic_links('#test')
        )

    def test_insert_magic_replaces_prefix_hashtag(self):
        self.assertEqual(
            'prefix <a href="/h/test">#test</a>',
            insert_magic_links('prefix #test')
        )

    def test_insert_magic_replaces_hashtag_prefix_no_space(self):
        self.assertEqual(
            'prefix<a href="/h/test">#test</a>',
            insert_magic_links('prefix#test')
        )

    def test_insert_magic_replaces_hashtag_paren(self):
        self.assertEqual(
            'prefix(<a href="/h/test">#test</a>)',
            insert_magic_links('prefix(#test)')
        )

    def test_insert_magic_replaces_hashtag_underscore(self):
        self.assertEqual(
            'Dwitter is just <a href="/h/amazing_underscore">#amazing_underscore</a>, right?',
            insert_magic_links('Dwitter is just #amazing_underscore, right?')
        )

    def test_insert_magic_replaces_hashtag_illegal_hyphen(self):
        self.assertEqual(
            'Dwitter is just <a href="/h/amaze">#amaze</a>-balls, right?',
            insert_magic_links('Dwitter is just #amaze-balls, right?')
        )

    def test_insert_magic_hashtag_not_start_with_digit(self):
        self.assertEqual(
            'Dwitter is just #1337 or <a href="/h/super1337">#super1337</a>?',
            insert_magic_links('Dwitter is just #1337 or #super1337?')
        )

    def test_insert_magic_single_character_hashtag(self):
        self.assertEqual(
            '<a href="/h/s">#s</a>',
            insert_magic_links('#s')
        )
        self.assertEqual(
            '<a href="/h/S">#S</a>',
            insert_magic_links('#S')
        )
        self.assertEqual(
            '#1',  # Start with digit not legal
            insert_magic_links('#1')
        )

    # mixed

    def test_insert_magic_links_mixed(self):
        self.assertEqual(
            '<a href="/u/john">u/john</a> remixed '
            '<a href="/d/123">d/123</a> by '
            '<a href="/u/jane">u/jane</a>',
            insert_magic_links('u/john remixed d/123 by /u/jane')
        )

    def test_insert_magic_links_mixed_hashtag(self):
        self.assertEqual(
            '<a href="/h/awesome">#awesome</a> '
            '<a href="/u/john">u/john</a> remixed '
            '<a href="/h/amazing">#amazing</a> '
            '<a href="/d/123">d/123</a> by '
            '<a href="/u/jane">u/jane</a>'
            '<a href="/h/yey">#yey</a>',
            insert_magic_links('#awesome u/john remixed #amazing d/123 by /u/jane#yey')
        )
