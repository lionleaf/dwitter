from django.test import TransactionTestCase, Client
from django.contrib.auth.models import User
from dwitter.models import Dweet
from django.utils import timezone


def assertResponse(self, response=None, status_code=None, templates=None):
    self.assertEqual(response.status_code, status_code)
    self.assertEqual([template.name for template in response.templates],
                     templates)


class DweetTestCase(TransactionTestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='dweet.localhost:8000')
        self.user = User.objects.create(username="user", password="")
        self.dweet = Dweet.objects.create(id=1,
                                          code="dweet code",
                                          posted=timezone.now(),
                                          author=self.user)

    def test_fullscreen_dweet_returns_404_if_dweet_does_not_exist(self):
        response = self.client.get('/id/2')
        assertResponse(self,
                       response=response,
                       status_code=404,
                       templates=['404_dweet.html'])

    def test_fullscreen_dweet_returns_dweet_with_correct_code(self):
        response = self.client.get('/id/1')
        assertResponse(self,
                       response=response,
                       status_code=200,
                       templates=['dweet/dweet.html'])

    def test_blank_dweet_renders_with_correct_template(self):
        response = self.client.get('/blank')
        assertResponse(self,
                       response=response,
                       status_code=200,
                       templates=['dweet/dweet.html'])
