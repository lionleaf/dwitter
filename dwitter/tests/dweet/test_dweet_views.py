from django.test import TransactionTestCase, Client
from django.contrib.auth.models import User
from dwitter.models import Dweet
from django.utils import timezone


class DweetTestCase(TransactionTestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='dweet.example.com')
        self.user = User.objects.create(username="user", password="")
        self.dweet = Dweet.objects.create(id=1,
                                          code="dweet code",
                                          posted=timezone.now(),
                                          _author=self.user)

    def test_fullscreen_dweet_returns_404_if_dweet_does_not_exist(self):
        response = self.client.get('/id/2')
        self.assertEqual(response.status_code, 404)
        with open('dwitter/templates/404_dweet.html') as f:
            self.assertEqual(response.content, f.read())

    def test_fullscreen_dweet_returns_dweet_with_correct_code(self):
        response = self.client.get('/id/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.dweet.code, response.content)

    def test_blank_dweet_renders_with_correct_template(self):
        response = self.client.get('/blank')
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.context['code'], response.content)
