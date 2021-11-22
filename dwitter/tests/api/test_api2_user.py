from django.test import Client, TransactionTestCase
from django.contrib.auth.models import User
import json

APIV2_PATH = '/apiv2beta'


class Api2UserRegistrationTestCase(TransactionTestCase):
    def setUp(self):
        self.client = Client()

    def register_user(self, username, email, password, password2):
        return self.client.post(f'{APIV2_PATH}/users/',
                                {'username': username, 'email': email,
                                 'password': password, 'password2': password2})

    def login(self, username, password):
        return self.client.post(f'{APIV2_PATH}/api-token-auth/',
                                {'username': username, 'password': password})

    def post_dweet(self, token, code, comment):
        return self.client.post(f'{APIV2_PATH}/dweets/',
                                {'code': code, 'first-comment': comment},
                                HTTP_AUTHORIZATION='token ' + token)

    def test_valid_registration(self):
        response = self.register_user('user1', 'user1@example.com', 'user1Pass', 'user1Pass')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='user1').exists())

        newUser = User.objects.get(username='user1')
        self.assertEqual(newUser.email, 'user1@example.com')
        self.assertTrue(newUser.check_password('user1Pass'))

        # Log in and post a dweet with new user
        response = self.login('user1', 'user1Pass')
        self.assertEquals(response.status_code, 200)
        token = json.loads(response.content)['token']
        response = self.post_dweet(token, 'coooode', 'hello')
        self.assertEquals(response.status_code, 200)

    def test_empty(self):
        response = self.register_user('', '', '', '')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)

    def test_username_too_long(self):
        response = self.register_user('1234567890' * 16, 'email@example.com',
                                      'user1Pass', 'user1Pass')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)

    def test_email_long_but_valid(self):
        # Django allows 254 character long emails
        email = 'a'*64 + '@' + 'b' * 63 + '.com'
        response = self.register_user('user1', email, 'user1Pass', 'user1Pass')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='user1').exists())

        newUser = User.objects.get(username='user1')
        self.assertEqual(newUser.email, email)
        self.assertTrue(newUser.check_password('user1Pass'))

    def test_email_required(self):
        response = self.register_user('user1', '', 'user1Pass', 'user1Pass')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)

    def test_email_too_long(self):
        response = self.register_user('user1', 'a'*256 + '@example.com', 'user1Pass', 'user1Pass')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)

    def test_email_invalid(self):
        response = self.register_user('user1', 'invalid_email', 'user1Pass', 'user1Pass')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)

    def test_password_long_but_valid(self):
        password = 'u1P!'*32  # 128 character long password
        response = self.register_user('user1', 'user1@example.com', password, password)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='user1').exists())

        newUser = User.objects.get(username='user1')
        self.assertEqual(newUser.email, 'user1@example.com')
        self.assertTrue(newUser.check_password(password))

    def test_password_required(self):
        response = self.register_user('user1', 'user1@example.com', '', '')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)

    def test_password_different(self):
        response = self.register_user('user1', 'user1@example.com', 'user1Pass', 'differentPass2')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)

    def test_password_too_short(self):
        response = self.register_user('user1', 'user1@example.com', 'user', 'user')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)

    def test_change_email(self):
        response = self.register_user('user1', 'user1@example.com', 'user1Pass', 'user1Pass')
        self.assertEquals(response.status_code, 201)

        response = self.login('user1', 'user1Pass')
        self.assertEquals(response.status_code, 200)

        token = 'token ' + json.loads(response.content)['token']
        response = self.client.post(f'{APIV2_PATH}/users/me/set_email/',
                                    {'email': 'different@example.com'}, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username='user1')
        self.assertEqual(user.email, 'different@example.com')

    def test_change_password(self):
        response = self.register_user('user1', 'user1@example.com', 'user1Pass', 'user1Pass')
        self.assertEquals(response.status_code, 201)

        response = self.login('user1', 'user1Pass')
        self.assertEquals(response.status_code, 200)

        token = 'token ' + json.loads(response.content)['token']

        # Wrong old pass first
        response = self.client.post(f'{APIV2_PATH}/users/me/set_password/',
                                    {'old_password': 'wrong',
                                     'new_password': 'newPass'},
                                    HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 400)

        # No old pass first
        response = self.client.post(f'{APIV2_PATH}/users/me/set_password/',
                                    {'new_password': 'newPass'},
                                    HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 400)

        # Correct attempt
        response = self.client.post(f'{APIV2_PATH}/users/me/set_password/',
                                    {'old_password': 'user1Pass',
                                     'new_password': 'newPassword3'},
                                    HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username='user1')
        self.assertTrue(user.check_password('newPassword3'))


class Api2UserGetTestCase(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='user1Pass',
        )

    def get_user(self, user_id):
        return self.client.get(f'{APIV2_PATH}/users/{str(user_id)}/')

    def test_invalid_user(self):
        response = self.get_user('invalid_user')
        self.assertEqual(response.status_code, 404)

    def test_valid_user(self):
        response = self.get_user(self.user1.id)
        self.assertContains(response, 'user1')
        self.assertContains(response, 'avatar')

    def test_no_email_leak(self):
        response = self.get_user(self.user1.id)
        self.assertNotContains(response, 'email')
        self.assertNotContains(response, 'example.com')

    def test_no_password_leak(self):
        response = self.get_user(self.user1.id)
        self.assertNotContains(response, 'password')
        # user1.password is the hash of the password,
        # which we obviously don't want to return
        self.assertNotContains(response, self.user1.password)


class Api2UserInvalidMethodsTestCase(TransactionTestCase):
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

        # Log in with user1
        response = self.login('user1', 'user1Pass')
        self.authUser1 = 'token ' + json.loads(response.content)['token']

        response = self.login('user2', 'user2Pass')
        self.authUser2 = 'token ' + json.loads(response.content)['token']

    def login(self, username, password):
        return self.client.post(f'{APIV2_PATH}/api-token-auth/',
                                {'username': username, 'password': password})

    def test_no_delete(self):
        # Without authentication
        self.assertEqual(User.objects.count(), 2)
        response = self.client.delete(f'{APIV2_PATH}/users/{str(self.user1.id)}/')
        self.assertEqual(response.status_code, 405)

        # Delete self with authentication
        response = self.client.delete(
            f'{APIV2_PATH}/users/{str(self.user1.id)}/', HTTP_AUTHORIZATION=self.authUser1)
        self.assertEqual(response.status_code, 405)

        # Delete other with authentication
        response = self.client.delete(
            f'{APIV2_PATH}/users/{str(self.user1.id)}/', HTTP_AUTHORIZATION=self.authUser2)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(User.objects.count(), 2)

    def test_no_patch(self):
        response = self.client.patch(f'{APIV2_PATH}/users/{str(self.user1.id)}/',
                                     json.dumps({'username': 'user2', 'email': 'user2@example.com',
                                                 'password': 'user2Pas', 'password2': 'user2Pas'}),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 405)

        response = self.client.patch(f'{APIV2_PATH}/users/{str(self.user1.id)}/',
                                     json.dumps({'username': 'user2', 'email': 'user2@example.com',
                                                 'password': 'user2Pas', 'password2': 'user2Pas'}),
                                     content_type="application/json",
                                     HTTP_AUTHORIZATION=self.authUser1)
        self.assertEqual(response.status_code, 405)

        response = self.client.patch(f'{APIV2_PATH}/users/{str(self.user1.id)}/',
                                     json.dumps({'username': 'user2', 'email': 'user2@example.com',
                                                 'password': 'user2Pas', 'password2': 'user2Pas'}),
                                     content_type="application/json",
                                     HTTP_AUTHORIZATION=self.authUser2)
        self.assertEqual(response.status_code, 405)

        user = User.objects.get(id=self.user1.id)
        self.assertEqual(user.username, 'user1')
        self.assertEqual(user.email, 'user1@example.com')
        self.assertTrue(user.check_password('user1Pass'))

    def test_empty_patch(self):
        response = self.client.patch(f'{APIV2_PATH}/users/{str(self.user1.id)}/')
        self.assertEqual(response.status_code, 405)
        response = self.client.patch(
            f'{APIV2_PATH}/users/{str(self.user1.id)}/', HTTP_AUTHORIZATION=self.authUser1)
        self.assertEqual(response.status_code, 405)

    def test_empty_post(self):
        response = self.client.post(
            f'{APIV2_PATH}/users/{str(self.user1.id)}/', HTTP_AUTHORIZATION=self.authUser1)
        self.assertEqual(response.status_code, 405)
        response = self.client.post(f'{APIV2_PATH}/users/{str(self.user1.id)}/')
        self.assertEqual(response.status_code, 405)

        response = self.client.post(f'{APIV2_PATH}/users/', HTTP_AUTHORIZATION=self.authUser1)
        self.assertEqual(response.status_code, 400)
        response = self.client.post(f'{APIV2_PATH}/users/')
        self.assertEqual(response.status_code, 400)

    def test_no_put(self):
        response = self.client.put(f'{APIV2_PATH}/users/{str(self.user1.id)}/')
        self.assertEqual(response.status_code, 405)
        response = self.client.put(
            f'{APIV2_PATH}/users/{str(self.user1.id)}/', HTTP_AUTHORIZATION=self.authUser1)
        self.assertEqual(response.status_code, 405)

    def test_no_list(self):
        response = self.client.get(f'{APIV2_PATH}/users/')
        self.assertEqual(response.status_code, 405)
        response = self.client.get(f'{APIV2_PATH}/users/', HTTP_AUTHORIZATION=self.authUser1)
        self.assertEqual(response.status_code, 405)

    def test_no_set_email_without_auth(self):
        response = self.client.post(f'{APIV2_PATH}/users/{str(self.user1.id)}/set_email/',
                                    {'email': 'evil@example.com'})
        self.assertEqual(response.status_code, 403)

        # Logged in as different user
        response = self.client.post(f'{APIV2_PATH}/users/{str(self.user1.id)}/set_email/',
                                    {'email': 'evil@example.com'},
                                    HTTP_AUTHORIZATION=self.authUser2)
        self.assertEqual(response.status_code, 403)

        user = User.objects.get(id=self.user1.id)
        self.assertEqual(user.email, 'user1@example.com')

    def test_no_set_password_without_auth(self):
        response = self.client.post(f'{APIV2_PATH}/users/{str(self.user1.id)}/set_password/',
                                    {'old_password': 'user1Pass', 'new_password': 'evilPass123'})
        self.assertEqual(response.status_code, 403)

        response = self.client.post(f'{APIV2_PATH}/users/{str(self.user1.id)}/set_password/',
                                    {'old_password': 'user1Pass', 'new_password': 'evilPass123'},
                                    HTTP_AUTHORIZATION=self.authUser2)
        self.assertEqual(response.status_code, 403)

        user = User.objects.get(id=self.user1.id)
        self.assertTrue(user.check_password('user1Pass'))
