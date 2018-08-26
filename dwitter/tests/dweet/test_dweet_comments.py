import json

from django.contrib.auth.models import User
from django.test import Client, TransactionTestCase
from django.utils import timezone
from django.utils.html import escape

from dwitter.models import Comment, Dweet


def code_wrap(s):
    if s.startswith('`') and s.endswith('`'):
        return '<code>%s</code>' % s[1:-1]


class DweetTestCase(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="user", password="")
        self.dweet = Dweet.objects.create(
            id=1,
            code="dweet code",
            posted=timezone.now(),
            author=self.user)

    def create_comment(self, text):
        return Comment.objects.create(
            text=text,
            posted=timezone.now(),
            reply_to=self.dweet,
            author=self.user)

    def get_dweet(self):
        response = self.client.get('/d/%d' % self.dweet.id)
        self.assertEqual(response.status_code, 200)
        return response

    def get_comments_ajax(self):
        response = self.client.get('/api/comments/?format=json&reply_to=%d' % self.dweet.id)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content)['results']

    def test_comment(self):
        comment = self.create_comment('this is a comment!')
        response = self.get_dweet()
        self.assertContains(response, comment.text)

    def test_comment_xss(self):
        comment = self.create_comment('<test>this is a comment!</test>')
        response = self.get_dweet()
        self.assertNotContains(response, '<test>')
        self.assertContains(response, escape(comment.text))

    def test_comment_code_blocks(self):
        comment = self.create_comment('`this is a comment!`')
        response = self.get_dweet()
        self.assertContains(response, code_wrap(comment.text))

    def test_comment_code_blocks_xss(self):
        comment = self.create_comment('`<test>this is a comment!</test>`')
        response = self.get_dweet()
        self.assertNotContains(response, '<test>')
        self.assertContains(response, code_wrap(escape(comment.text)))

    def test_comment_ajax(self):
        comment = self.create_comment('this is a comment!')
        response = self.get_comments_ajax()
        urlized_text = response[0]['urlized_text']
        self.assertEqual(comment.text, urlized_text)

    def test_comment_ajax_xss(self):
        comment = self.create_comment('<test>this is a comment!</test>')
        response = self.get_comments_ajax()
        urlized_text = response[0]['urlized_text']
        self.assertNotIn('<test>', urlized_text)
        self.assertEqual(escape(comment.text), urlized_text)

    def test_comment_code_blocks_ajax(self):
        comment = self.create_comment('`this is a comment!`')
        response = self.get_comments_ajax()
        urlized_text = response[0]['urlized_text']
        self.assertEqual(code_wrap(comment.text), urlized_text)

    def test_comment_code_blocks_ajax_xss(self):
        comment = self.create_comment('`<test>this is a comment!</test>`')
        response = self.get_comments_ajax()
        urlized_text = response[0]['urlized_text']
        self.assertNotIn('<test>', urlized_text)
        self.assertEqual(code_wrap(escape(comment.text)), urlized_text)
