from django.test import TestCase
from dwitter.templatetags.insert_magic_links import insert_magic_links


class DweetTestCase(TestCase):

    def test_insert_magic_bypasses_html(self):
        self.assertEqual(
            'prefix <h1>content</h1> suffix',
            insert_magic_links('prefix <h1>content</h1> suffix')
        )

    # user

    def test_insert_magic_replaces_user_valid_characters(self):
        self.assertEqual(
            '<a href="/u/a1_.@+-">u/a1_.@+-</a>',
            insert_magic_links('u/a1_.@+-')
        )

    def test_insert_magic_bypasses_user_invalid_characters(self):
        self.assertEqual(
            'u/a1$',
            insert_magic_links('u/a1$')
        )

    def test_insert_magic_replaces_standalone_user(self):
        self.assertEqual(
            '<a href="/u/a">u/a</a>',
            insert_magic_links('u/a')
        )

    def test_insert_magic_replaces_user_at_start_of_string(self):
        self.assertEqual(
            '<a href="/u/a">u/a</a> suffix',
            insert_magic_links('u/a suffix')
        )

    def test_insert_magic_replaces_user_at_end_of_string(self):
        self.assertEqual(
            'prefix <a href="/u/a">u/a</a>',
            insert_magic_links('prefix u/a')
        )

    def test_insert_magic_replaces_user_at_middle_of_string(self):
        self.assertEqual(
            'prefix <a href="/u/a">u/a</a> suffix',
            insert_magic_links('prefix u/a suffix')
        )

    def test_insert_magic_bypasses_user_prefixed_by_non_space(self):
        self.assertEqual(
            'prefixu/a suffix',
            insert_magic_links('prefixu/a suffix')
        )

    def test_insert_magic_bypasses_user_suffixed_by_non_space(self):
        self.assertEqual(
            'prefix u/a/suffix',
            insert_magic_links('prefix u/a/suffix')
        )

    def test_insert_magic_replaces_user_prefixed_by_slash(self):
        self.assertEqual(
            'prefix <a href="/u/a">u/a</a> prefix/u/a',
            insert_magic_links('prefix /u/a prefix/u/a')
        )

    def test_insert_magic_replaces_user_inside_parenthases(self):
        self.assertEqual(
            '(<a href="/u/a">u/a</a>)',
            insert_magic_links('(u/a)')
        )

    # test that username mentions follow the new punctuation rules
    def test_user_mention_punctuation(self):
        self.assertEqual(
            "are you there, <a href='/u/admin'>u/admin</a>?"
            "hello <a href='/u/ser'>u/ser</a>!"
            "check out this comment from <a href='/u/person'>u/person</a>:"
            "<a href='/u/1a'>u/1a</a> and "
            "<a href='/u/2b'>u/2b</a> are the top dwitter users"
            "<a href='/u/tobe'>u/tobe</a>; or <a href='/u/nottobe'>u/nottobe</a>, "
            "that is the <a href='/u/question'>u/question</a>."
            "u/1am1nv4L1D##@$",
            insert_magic_links(
                "are you there, u/admin?"
                "hello u/ser!"
                "check out this comment from u/person:"
                "u/1a and u/2b are the top dwitter users"
                "u/tobe; or u/nottobe, that is the u/question."
                "u/1am1nv4L1D##@$"
            )
        )

    # autocrop (https://dwitter.net/d/1 -> d/1)

    def test_insert_magic_autocrops_urls_d(self):
        self.assertEqual(
            '<a href="/d/123">d/123</a>',
            insert_magic_links('dwitter.net/d/123')
        )

    def test_insert_magic_autocrops_urls_d_https(self):
        self.assertEqual(
            '<a href="/d/123">d/123</a>',
            insert_magic_links('https://dwitter.net/d/123')
        )

    def test_insert_magic_autocrops_urls_d_www(self):
        self.assertEqual(
            '<a href="/d/123">d/123</a>',
            insert_magic_links('www.dwitter.net/d/123')
        )

    def test_insert_magic_autocrops_urls_d_https_www(self):
        self.assertEqual(
            '<a href="/d/123">d/123</a>',
            insert_magic_links('https://www.dwitter.net/d/123')
        )

    def test_insert_magic_autocrops_urls_d_mixed(self):
        self.assertEqual(
            '<a href="/d/123">d/123</a> <a href="/d/456">456</a>',
            insert_magic_links('dwitter.net/d/123 http://dwitter.net/d/456')
        )

    # autocrop with u/ links

    def test_insert_magic_autocrops_urls_u(self):
        self.assertEqual(
            '<a href="/u/yonatan">u/yonatan</a>',
            insert_magic_links('dwitter.net/u/yonatan')
        )

    def test_insert_magic_autocrops_urls_u_https(self):
        self.assertEqual(
            '<a href="/u/veubeke">u/veubeke</a>',
            insert_magic_links('https://dwitter.net/u/veubeke')
        )

    def test_insert_magic_autocrops_urls_u_www(self):
        self.assertEqual(
            '<a href="/u/pavel">u/pavel</a>',
            insert_magic_links('www.dwitter.net/u/pavel')
        )

    def test_insert_magic_autocrops_urls_u_https_www(self):
        self.assertEqual(
            '<a href="/u/lionleaf">u/lionleaf</a>',
            insert_magic_links('https://www.dwitter.net/u/lionleaf')
        )

    def test_insert_magic_autocrops_urls_u_mixed(self):
        self.assertEqual(
            '<a href="/u/sigveseb">u/sigveseb</a> <a href="/u/aemkei">u/aemkei</a>',
            insert_magic_links('dwitter.net/u/sigveseb http://dwitter.net/u/aemkei')
        )

    def test_insert_magic_autocrop_with_text(self):
        self.assertEqual(
            'Whoa, have you seen the dweets <a href="/u/sigveseb">u/sigveseb</a> makes?',
            insert_magic_links('Whoa, have you seen the dweets dwitter.net/u/sigveseb makes?')
        )

    # autocrop with http:// - in case someone forgets themselves

    def test_insert_magic_autocrops_urls_http_d(self):
        self.assertEqual(
            '<a href="/d/123">d/123</a>',
            insert_magic_links('http://dwitter.net/d/123')
        )

    def test_insert_magic_autocrops_urls_http_u(self):
        self.assertEqual(
            '<a href="/u/lionleaf">u/lionleaf</a>',
            insert_magic_links('http://www.dwitter.net/u/lionleaf')
        )

    # prefixed autocrops

    def test_insert_magic_autocrop_bypasses_urls_prefixed(self):
        self.assertEqual(
            'prefixhttp://dwitter.net/d/123',
            insert_magic_links('prefixhttp://dwitter.net/d/123')
        )

    # dweet

    def test_insert_magic_replaces_dweet_valid_characters(self):
        self.assertEqual(
            '<a href="/d/1234567890">d/1234567890</a>',
            insert_magic_links('d/1234567890')
        )

    def test_insert_magic_bypasses_dweet_invalid_characters(self):
        self.assertEqual(
            'd/1a$',
            insert_magic_links('d/1a$')
        )

    def test_insert_magic_replaces_standalone_dweet(self):
        self.assertEqual(
            '<a href="/d/1">d/1</a>',
            insert_magic_links('d/1')
        )

    def test_insert_magic_replaces_dweet_at_start_of_string(self):
        self.assertEqual(
            '<a href="/d/1">d/1</a> suffix',
            insert_magic_links('d/1 suffix')
        )

    def test_insert_magic_replaces_dweet_at_end_of_string(self):
        self.assertEqual(
            'prefix <a href="/d/1">d/1</a>',
            insert_magic_links('prefix d/1')
        )

    def test_insert_magic_replaces_dweet_at_middle_of_string(self):
        self.assertEqual(
            'prefix <a href="/d/1">d/1</a> suffix',
            insert_magic_links('prefix d/1 suffix')
        )

    def test_insert_magic_bypasses_dweet_prefixed_by_non_space(self):
        self.assertEqual(
            'prefixd/1 suffix',
            insert_magic_links('prefixd/1 suffix')
        )

    def test_insert_magic_bypasses_dweet_suffixed_by_non_space(self):
        self.assertEqual(
            'prefix d/1/suffix',
            insert_magic_links('prefix d/1/suffix')
        )

    def test_insert_magic_replaces_dweet_prefixed_by_slash(self):
        self.assertEqual(
            'prefix <a href="/d/1">d/1</a> prefix/d/1',
            insert_magic_links('prefix /d/1 prefix/d/1')
        )

    def test_insert_magic_replaces_dweet_in_parentheses(self):
        self.assertEqual(
            '(<a href="/d/1">d/1</a>)',
            insert_magic_links('(d/1)')
        )

    # test that dweet mentions follow the same punctuation rules as usernames, et cetera
    def test_insert_magic_dweet_punctuation(self):
        self.assertEqual(
            "I love <a href='/d/123'>d/123</a>, "
            "but have you seen <a href='/d/456'>d/456</a>?",
            insert_magic_links('I love d/123, but have you seen d/456?')
        )

    # hashtag

    def test_insert_magic_replaces_basic_hashtag(self):
        self.assertEqual(
            '<a href="/h/test">#test</a>',
            insert_magic_links('#test')
        )

    def test_insert_magic_replaces_hashtag_space_prefix(self):
        self.assertEqual(
            'prefix <a href="/h/test">#test</a>',
            insert_magic_links('prefix #test')
        )

    def test_insert_magic_bypasses_hashtag_prefix_no_space(self):
        self.assertEqual(
            'prefix#test',
            insert_magic_links('prefix#test')
        )

    def test_insert_magic_replaces_hashtag_underscore(self):
        self.assertEqual(
            'Dwitter is just <a href="/h/amazing_underscore">#amazing_underscore</a>, right?',
            insert_magic_links('Dwitter is just #amazing_underscore, right?')
        )

    def test_insert_magic_bypasses_hashtag_illegal_hyphen(self):
        self.assertEqual(
            'Dwitter is just #amaze-balls, right?',
            insert_magic_links('Dwitter is just #amaze-balls, right?')
        )

    def test_insert_magic_bypasses_hashtag_no_letters(self):
        self.assertEqual(
            'Dwitter is so #1337',
            insert_magic_links('Dwitter is so #1337')
        )

    def test_insert_magic_replaces_hashtag_digits_then_letters(self):
        self.assertEqual(
            'We are the <a href="/h/1337elite">#1337elite</a>',
            insert_magic_links('We are the #1337elite')
        )

    def test_insert_magic_hashtag_letters_and_digits(self):
        self.assertEqual(
            'Dwitter is like <a href="/h/abc123">#abc123</a>',
            insert_magic_links('Dwitter is like #abc123')
        )

    def test_insert_magic_single_character_hashtag(self):
        self.assertEqual(
            '<a href="/h/h">#h</a>',
            insert_magic_links('#h')
        )
        self.assertEqual(
            '<a href="/h/H">#H</a>',
            insert_magic_links('#H')
        )

    # test that hashtags follow the same punctuation rules as usernames, et cetera
    def test_insert_magic_hashtag_punctuation(self):
        self.assertEqual(
            "<a href='/h/hash'>#hash</a>, but also <a href='/h/tag'>#tag</a>. Not #tag$%",
            insert_magic_links('#hash, but also #tag. Not #tag$%')
        )

    # mixed

    def test_insert_magic_mixed(self):
        self.assertEqual(
            '<a href="/u/john">u/john</a> remixed '
            '<a href="/d/123">d/123</a> by '
            '<a href="/u/jane">u/jane</a>',
            insert_magic_links('u/john remixed d/123 by /u/jane')
        )

    def test_insert_magic_mixed_hashtag(self):
        self.assertEqual(
            '<a href="/h/awesome">#awesome</a> '
            '<a href="/u/john">u/john</a> remixed '
            '<a href="/h/amazing">#amazing</a> '
            '<a href="/d/123">d/123</a> by '
            '<a href="/u/jane">u/jane</a>'
            '#yey',
            insert_magic_links('#awesome u/john remixed #amazing d/123 by /u/jane#yey')
        )
