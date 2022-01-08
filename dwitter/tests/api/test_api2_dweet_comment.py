from django.test import Client, TransactionTestCase
from django.contrib.auth.models import User
from django.utils import timezone
from dwitter.models import Comment, Dweet
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


class Api2DweetAndCommentDeletionTestCase(Api2BaseTestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='user1Pass',
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='user2Pass',
        )
        self.mod = User.objects.create_user(
            username='mod',
            email='mod@example.com',
            password='banHammer69',
            is_staff=True  # set the mod flag
        )
        self.dweet1 = Dweet.objects.create(id=1,
                                           code="dweet code",
                                           posted=timezone.now(),
                                           author=self.user1)

        # log in with both users
        token = self.login('user1', 'user1Pass')
        self.authUser1 = 'token ' + token

        token = self.login('user2', 'user2Pass')
        self.authUser2 = 'token ' + token

        token = self.login('mod', 'banHammer69')
        self.authMod = 'token ' + token

    def test_dweet_deletion(self):
        self.dweet2 = Dweet.objects.create(id=2,
                                           code="dweet code",
                                           posted=timezone.now(),
                                           author=self.user2)

        self.dweetmod = Dweet.objects.create(id=3,
                                             code="dweet code",
                                             posted=timezone.now(),
                                             author=self.mod)

        self.assertEqual(Dweet.objects.count(), 3)
        # Without authentication
        response = self.client.delete(f'{APIV2_PATH}/dweets/{str(self.dweet1.id)}/')
        self.assertEqual(response.status_code, 403)

        # Delete other user's dweet with authentication should fail
        response = self.client.delete(
            f'{APIV2_PATH}/dweets/{str(self.dweet1.id)}/', HTTP_AUTHORIZATION=self.authUser2)
        self.assertEqual(response.status_code, 403)

        # Delete mod's dweet with authentication should fail for other users
        response = self.client.delete(
            f'{APIV2_PATH}/dweets/{str(self.dweetmod.id)}/', HTTP_AUTHORIZATION=self.authUser1)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Dweet.objects.count(), 3)

        # Delete self should work
        response = self.client.delete(
            f'{APIV2_PATH}/dweets/{str(self.dweet1.id)}/', HTTP_AUTHORIZATION=self.authUser1)
        self.assertEqual(response.status_code, 204)

        # Delete other's dweet should work if you're a moderator
        response = self.client.delete(
            f'{APIV2_PATH}/dweets/{str(self.dweet2.id)}/', HTTP_AUTHORIZATION=self.authMod)
        self.assertEqual(response.status_code, 204)

        # Delete mod self dweet should work
        response = self.client.delete(
            f'{APIV2_PATH}/dweets/{str(self.dweetmod.id)}/', HTTP_AUTHORIZATION=self.authMod)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Dweet.objects.count(), 0)

    def test_comment_deletion(self):
        self.comment1 = Comment.objects.create(id=1,
                                               posted=timezone.now(),
                                               reply_to=self.dweet1,
                                               author=self.user1)
        self.comment2 = Comment.objects.create(id=2,
                                               posted=timezone.now(),
                                               reply_to=self.dweet1,
                                               author=self.user2)
        self.commentMod = Comment.objects.create(id=3,
                                                 posted=timezone.now(),
                                                 reply_to=self.dweet1,
                                                 author=self.mod)

        self.assertEqual(Comment.objects.count(), 3)

        # Without authentication
        response = self.client.delete(f'{APIV2_PATH}/comments/{str(self.comment1.id)}/')
        self.assertEqual(response.status_code, 403)

        # Delete other user's comment with authentication should fail
        response = self.client.delete(
            f'{APIV2_PATH}/comments/{str(self.comment1.id)}/', HTTP_AUTHORIZATION=self.authUser2)
        self.assertEqual(response.status_code, 403)

        # Delete mod's comment with authentication should fail for other users
        response = self.client.delete(
            f'{APIV2_PATH}/comments/{str(self.commentMod.id)}/', HTTP_AUTHORIZATION=self.authUser2)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Comment.objects.count(), 3)

        # Delete self should work
        response = self.client.delete(
            f'{APIV2_PATH}/comments/{str(self.comment1.id)}/', HTTP_AUTHORIZATION=self.authUser1)
        self.assertEqual(response.status_code, 204)

        # Delete other's dweet should work if you're a moderator
        response = self.client.delete(
            f'{APIV2_PATH}/comments/{str(self.comment2.id)}/', HTTP_AUTHORIZATION=self.authMod)
        self.assertEqual(response.status_code, 204)

        # Delete mod self dweet should work
        response = self.client.delete(
            f'{APIV2_PATH}/comments/{str(self.commentMod.id)}/', HTTP_AUTHORIZATION=self.authMod)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Comment.objects.count(), 0)
