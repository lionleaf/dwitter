from django.test import Client, TransactionTestCase
from django.contrib.auth.models import User
from django.utils import timezone
from dwitter.models import Dweet
import json

APIV2_PATH = '/apiv2beta'


class Api2BaseTestCase(TransactionTestCase):
    def login(self, username, password):
        response = self.client.post(f'{APIV2_PATH}/api-token-auth/',
                                    {'username': username, 'password': password})
        self.assertEquals(response.status_code, 200)
        token = json.loads(response.content)['token']
        return token

    def post_dweet(self, token, code, comment):
        return self.client.post(f'{APIV2_PATH}/dweets/',
                                {'code': code, 'first-comment': comment},
                                content_type='application/json',
                                HTTP_AUTHORIZATION='token ' + token)

    def post_comment(self, token, dweet_id, comment):
        return self.client.post(f'{APIV2_PATH}/dweets/{dweet_id}/add_comment/',
                                {'text': comment},
                                content_type='application/json',
                                HTTP_AUTHORIZATION='token ' + token)

    def set_like(self, token, dweet_id, like):
        return self.client.post(f'{APIV2_PATH}/dweets/{dweet_id}/set_like/',
                                {'like': like},
                                content_type='application/json',
                                HTTP_AUTHORIZATION='token ' + token)

    def get_dweet(self, dweet_id):
        return self.client.get(f'{APIV2_PATH}/dweets/{dweet_id}/',
                               content_type='application/json')

    def get_dweets(self):
        return self.client.get(f'{APIV2_PATH}/dweets/',
                               content_type='application/json')


class Api2DweetAndCommentCreateTestCase(Api2BaseTestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='user1Pass',
        )
        self.token1 = self.login('user1', 'user1Pass')

        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='user2Pass',
        )
        self.token2 = self.login('user2', 'user2Pass')

    def test_post_dweet(self):
        resp = self.post_dweet(self.token1, 'my sweet code', 'best dweet!')
        self.assertEquals(resp.status_code, 200)
        dweet = json.loads(resp.content)
        self.assertEquals(dweet['code'], 'my sweet code')
        self.assertEquals(dweet['comments'][0]['text'], 'best dweet!')
        self.assertEquals(dweet['author']['id'], self.user1.id)
        self.assertEquals(dweet['author']['username'], self.user1.username)

        # require login
        resp = self.post_dweet('no token', 'my sweet code', 'best dweet!')
        self.assertEquals(resp.status_code, 401)

    def test_post_comment(self):
        resp = self.post_dweet(self.token1, 'my sweet code', 'best dweet!')
        dweetId = json.loads(resp.content)['id']

        resp = self.post_comment(self.token1, dweetId, 'comment!')
        self.assertEquals(resp.status_code, 200)
        dweet = json.loads(resp.content)
        self.assertEquals(dweet['comments'][1]['text'], 'comment!')
        self.assertEquals(dweet['comments'][1]['author']['username'], 'user1')

        resp = self.post_comment(self.token2, dweetId, 'another comment!')
        self.assertEquals(resp.status_code, 200)
        dweet = json.loads(resp.content)
        self.assertEquals(dweet['comments'][2]['text'], 'another comment!')
        self.assertEquals(dweet['comments'][2]['author']['username'], 'user2')

    def test_set_like(self):
        resp = self.post_dweet(self.token1, 'my sweet code', 'best dweet!')
        dweet_id = json.loads(resp.content)['id']

        # Dweets start out self-liked
        dweet = json.loads(resp.content)
        self.assertEquals(dweet['has_user_awesomed'], True)
        self.assertEquals(dweet['awesome_count'], 1)

        # unlike
        resp = self.set_like(self.token1, dweet_id, False)
        self.assertEquals(resp.status_code, 200)
        dweet = json.loads(resp.content)
        self.assertEquals(dweet['awesome_count'], 0)
        self.assertEquals(dweet['has_user_awesomed'], False)

        # relike
        resp = self.set_like(self.token1, dweet_id, True)
        self.assertEquals(resp.status_code, 200)
        dweet = json.loads(resp.content)
        self.assertEquals(dweet['has_user_awesomed'], True)
        self.assertEquals(dweet['awesome_count'], 1)


class Api2DweetAndCommentGetTestCase(Api2BaseTestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='user1Pass',
        )
        self.token1 = self.login('user1', 'user1Pass')

        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='user2Pass',
        )
        self.token2 = self.login('user2', 'user2Pass')

        self.dweet1 = Dweet.objects.create(id=1,
                                           code="first code",
                                           posted=timezone.now(),
                                           author=self.user1)

        self.dweet2 = Dweet.objects.create(id=2,
                                           code="second code",
                                           posted=timezone.now(),
                                           author=self.user2)

    def test_get_dweets(self):
        resp = self.get_dweets()
        dweets = json.loads(resp.content)
        self.assertEquals(dweets['count'], 2)
        self.assertEquals(2, 2)

    def test_get_dweets_by_hashtag(self):
        # TODO
        return

    def test_get_dweets_by_username(self):
        # TODO
        return

    def test_get_dweets_pagination(self):
        # TODO
        return

    def test_get_dweets_by_period(self):
        # TODO
        return

    def test_get_dweets_random(self):
        # TODO
        return

    def test_get_dweets_hot(self):
        # TODO
        return

    def test_get_dweets_top(self):
        # TODO
        return

    def test_get_dweets_user(self):
        # TODO
        return

    def test_get_dweet(self):
        # TODO
        resp = self.get_dweet(2)
        self.assertEquals(resp.status_code, 200)

    def test_get_comments(self):
        # TODO
        return
