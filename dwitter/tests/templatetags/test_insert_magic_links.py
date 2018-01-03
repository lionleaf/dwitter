from django.test import TestCase
from dwitter.templatetags.insert_magic_links import insert_magic_links


class DweetTestCase(TestCase):
    def test_insert_magic_links_bypasses_html(self):
        self.assertEqual(
            'prefix <h1>content</h1> suffix',
            insert_magic_links('prefix <h1>content</h1> suffix')
        )

    def test_insert_magic_links_replaces_user_with_valid_characters(self):
        self.assertEqual(
            '<a href="/u/a1_.@+-">/u/a1_.@+-</a>',
            insert_magic_links('/u/a1_.@+-')
        )

    def test_insert_magic_links_bypasses_user_with_invalid_characters(self):
        self.assertEqual(
            '/u/a1$',
            '/u/a1$'
        )

    def test_insert_magic_links_replaces_standalone_user(self):
        self.assertEqual(
            '<a href="/u/a">/u/a</a>',
            insert_magic_links('/u/a')
        )

    def test_insert_magic_links_replaces_user_at_start_of_string(self):
        self.assertEqual(
            '<a href="/u/a">/u/a</a> suffix',
            insert_magic_links('/u/a suffix')
        )

    def test_insert_magic_links_replaces_user_at_end_of_string(self):
        self.assertEqual(
            'prefix <a href="/u/a">/u/a</a>',
            insert_magic_links('prefix /u/a')
        )

    def test_insert_magic_links_replaces_user_at_middle_of_string(self):
        self.assertEqual(
            'prefix <a href="/u/a">/u/a</a> suffix',
            insert_magic_links('prefix /u/a suffix')
        )

    def test_insert_magic_links_bypasses_user_prefixed_by_non_space(self):
        self.assertEqual(
            'prefix/u/a suffix',
            insert_magic_links('prefix/u/a suffix')
        )

    def test_insert_magic_links_bypasses_user_suffixed_by_non_space(self):
        self.assertEqual(
            'prefix /u/a/suffix',
            insert_magic_links('prefix /u/a/suffix')
        )

    def test_insert_magic_links_replaces_dweet_with_valid_characters(self):
        self.assertEqual(
            '<a href="/d/1234567890">/d/1234567890</a>',
            insert_magic_links('/d/1234567890')
        )

    def test_insert_magic_links_bypasses_dweet_with_invalid_characters(self):
        self.assertEqual(
            '/d/1a',
            '/d/1a'
        )

    def test_insert_magic_links_replaces_standalone_dweet(self):
        self.assertEqual(
            '<a href="/d/1">/d/1</a>',
            insert_magic_links('/d/1')
        )

    def test_insert_magic_links_replaces_dweet_at_start_of_string(self):
        self.assertEqual(
            '<a href="/d/1">/d/1</a> suffix',
            insert_magic_links('/d/1 suffix')
        )

    def test_insert_magic_links_replaces_dweet_at_end_of_string(self):
        self.assertEqual(
            'prefix <a href="/d/1">/d/1</a>',
            insert_magic_links('prefix /d/1')
        )

    def test_insert_magic_links_replaces_dweet_at_middle_of_string(self):
        self.assertEqual(
            'prefix <a href="/d/1">/d/1</a> suffix',
            insert_magic_links('prefix /d/1 suffix')
        )

    def test_insert_magic_links_bypasses_dweet_prefixed_by_non_space(self):
        self.assertEqual(
            'prefix/d/1 suffix',
            insert_magic_links('prefix/d/1 suffix')
        )

    def test_insert_magic_links_bypasses_dweet_suffixed_by_non_space(self):
        self.assertEqual(
            'prefix /d/1/suffix',
            insert_magic_links('prefix /d/1/suffix')
        )

    def test_insert_magic_links_mixed(self):
        self.assertEqual(
            '<a href="/u/john">/u/john</a> remixed '
            '<a href="/d/123">/d/123</a> by '
            '<a href="/u/jane">/u/jane</a>',
            insert_magic_links('/u/john remixed /d/123 by /u/jane')
        )
