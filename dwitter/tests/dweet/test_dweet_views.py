from django.test import TransactionTestCase, Client
from django.contrib.auth.models import User
from dwitter.models import Dweet
from dwitter.dweet.views import fullscreen_dweet, blank_dweet
from django.utils import timezone


def wrap_content(content):
    return 'function u(t) {\n       ' + content + '\n      }'


def assertResponse(self, response, **kwargs):
    self.assertEqual(response.resolver_match.func, kwargs['view'])
    self.assertEqual(response.status_code, kwargs['status_code'])
    self.assertEqual([template.name for template in response.templates],
                     kwargs['templates'])


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
        assertResponse(self, response,
                       view=fullscreen_dweet,
                       status_code=404,
                       templates=['404_dweet.html'])
        self.assertEqual(response.resolver_match.func, fullscreen_dweet)
        self.assertEqual(response.status_code, 404)
        self.assertEqual([template.name for template in response.templates],
                         ['404_dweet.html'])

    def test_fullscreen_dweet_returns_dweet_with_correct_code(self):
        response = self.client.get('/id/1')
        assertResponse(self, response,
                       view=fullscreen_dweet,
                       status_code=200,
                       templates=['dweet/dweet.html'])
        self.assertIn(wrap_content(self.dweet.code), response.content)

    def test_blank_dweet_renders_with_correct_template(self):
        response = self.client.get('/blank')
        assertResponse(self, response,
                       view=blank_dweet,
                       status_code=200,
                       templates=['dweet/dweet.html'])
        self.assertIn(wrap_content(response.context['code']), response.content)
