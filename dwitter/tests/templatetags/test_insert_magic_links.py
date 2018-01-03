from django.test import TestCase
from dwitter.templatetags.insert_magic_links import insert_magic_links


class DweetTestCase(TestCase):
    def test_insert_magic_links_bypasses_html(self):
        self.assertEqual('prefix <h1>content</h1> suffix', insert_magic_links('prefix <h1>content</h1> suffix'))

    def test_insert_magic_links_replaces_user_at_start_of_string(self):
        self.assertEqual('<a href="/u/username">/u/username</a> suffix', insert_magic_links('/u/username suffix'))

    def test_insert_magic_links_replaces_user_at_end_of_string(self):
        self.assertEqual('prefix <a href="/u/username">/u/username</a>', insert_magic_links('prefix /u/username'))

    def test_insert_magic_links_replaces_user_at_middle_of_string(self):
        self.assertEqual('prefix <a href="/u/username">/u/username</a> suffix', insert_magic_links('prefix /u/username suffix'))

    def test_insert_magic_links_bypasses_user_prefixed_by_non_whitespace(self):
        self.assertEqual('prefix/u/username suffix', insert_magic_links('prefix/u/username suffix'))

    def test_insert_magic_links_bypasses_user_suffixed_by_non_whitespace(self):
        self.assertEqual('prefix /u/username/suffix', insert_magic_links('prefix /u/username/suffix'))

    def test_insert_magic_links_replaces_dweet_at_start_of_string(self):
        self.assertEqual('<a href="/d/1">/d/1</a> suffix', insert_magic_links('/d/1 suffix'))

    def test_insert_magic_links_replaces_dweet_at_end_of_string(self):
        self.assertEqual('prefix <a href="/d/1">/d/1</a>', insert_magic_links('prefix /d/1'))

    def test_insert_magic_links_replaces_dweet_at_middle_of_string(self):
        self.assertEqual('prefix <a href="/d/1">/d/1</a> suffix', insert_magic_links('prefix /d/1 suffix'))

    def test_insert_magic_links_bypasses_dweet_prefixed_by_non_whitespace(self):
        self.assertEqual('prefix/d/1 suffix', insert_magic_links('prefix/d/1 suffix'))

    def test_insert_magic_links_bypasses_dweet_suffixed_by_non_whitespace(self):
        self.assertEqual('prefix /d/1/suffix', insert_magic_links('prefix /d/1/suffix'))
