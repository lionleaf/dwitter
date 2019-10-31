from django.test import TransactionTestCase, Client
from django.contrib.auth.models import User
from django.contrib import auth
from dwitter.models import Dweet, Comment, Hashtag
from django.utils import timezone


class PostDweetTestCase(TransactionTestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(username="user", password="invalid_pw_hash")
        self.user.set_password("hunter2")  # Created with proper hash so you can log in!
        self.user.save()

        self.dweet = Dweet.objects.create(id=1000,
                                          code="dweet code",
                                          posted=timezone.now(),
                                          author=self.user)

    def login(self):
        # Log in
        self.client.post('/accounts/login/',
                         {'username': 'user', 'password': 'hunter2'},
                         follow=True)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated, "Should be logged in after logging in")
        return user

    def test_post_new_dweet(self):
        user = self.login()

        response = self.client.post('/dweet', {'code': 'test_code'}, follow=True)
        self.assertEqual(response.status_code, 200,
                         "Posting dweet return 200. Status code " + str(response.status_code))

        dweet = Dweet.objects.get(code='test_code')
        self.assertEqual(dweet.code, 'test_code')
        self.assertEqual(dweet.author, user)

    def test_post_new_dweet_with_first_comment(self):
        user = self.login()

        response = self.client.post('/dweet',
                                    {'code': 'test_code', 'first-comment': 'hello there'},
                                    follow=True)
        self.assertEqual(response.status_code, 200,
                         "Posting dweet return 200. Status code " + str(response.status_code))

        dweet = Dweet.objects.get(code='test_code')
        self.assertEqual(dweet.code, 'test_code')
        self.assertEqual(dweet.author, user)
        comment = Comment.objects.get(reply_to=dweet)
        self.assertEqual(comment.text, 'hello there')
        self.assertEqual(comment.author, user)

    def test_post_new_dweet_with_first_comment_with_hashtag(self):
        user = self.login()

        response = self.client.post('/dweet',
                                    {'code': 'test_code', 'first-comment': 'hello there #woo'},
                                    follow=True)
        self.assertEqual(response.status_code, 200,
                         "Posting dweet return 200. Status code " + str(response.status_code))

        dweet = Dweet.objects.get(code='test_code')
        self.assertEqual(dweet.code, 'test_code')
        self.assertEqual(dweet.author, user)

        comment = Comment.objects.get(reply_to=dweet)
        self.assertEqual(comment.text, 'hello there #woo')
        self.assertEqual(comment.author, user)

        hashtag = Hashtag.objects.get(name='woo')
        self.assertEqual(dweet in hashtag.dweets.all(), True)

    def test_too_long_dweet_post(self):
        user = self.login()

        response = self.client.post('/dweet', {'code': 'test code that is way too long,' +
                                                       'wow this looks long in code.' +
                                                       'We could fit so much in here.' +
                                                       'oh wow. mooooooooooooooooar text.' +
                                                       'Getting there.' +
                                                       'And BAM tooo long!'}, follow=True)
        self.assertContains(response, "Dweet code too long!", status_code=400)

        # shorter code should go through!
        response = self.client.post('/dweet', {'code': 'test code that is a lot shorter,' +
                                                       'wow this looks long in code.' +
                                                       'And BAM not tooo long!'}, follow=True)
        self.assertEqual(response.status_code, 200)

        dweets = Dweet.objects.filter(author=user)
        self.assertEqual(dweets.count(), 2)

    def test_post_dweet_reply(self):
        user = self.login()

        response = self.client.post('/d/1000/reply', {'code': 'test_code'}, follow=True)
        self.assertEqual(response.status_code, 200,
                         "Posting dweet return 200. Status code " + str(response.status_code))

        dweet = Dweet.objects.get(code='test_code')
        self.assertEqual(dweet.code, 'test_code')
        self.assertEqual(dweet.author, user)
        self.assertEqual(dweet.reply_to, self.dweet)

    def test_post_dweet_reply_with_first_comment(self):
        user = self.login()

        response = self.client.post('/d/1000/reply',
                                    {'code': 'test_code', 'first-comment': 'hello there'},
                                    follow=True)
        self.assertEqual(response.status_code, 200,
                         "Posting dweet return 200. Status code " + str(response.status_code))

        dweet = Dweet.objects.get(code='test_code')
        self.assertEqual(dweet.code, 'test_code')
        self.assertEqual(dweet.author, user)
        self.assertEqual(dweet.reply_to, self.dweet)

        comment = Comment.objects.get(reply_to=dweet)
        self.assertEqual(comment.text, 'hello there')
        self.assertEqual(comment.author, user)

    def test_post_dweet_reply_with_first_comment_with_hashtag(self):
        user = self.login()

        response = self.client.post('/d/1000/reply',
                                    {'code': 'test_code', 'first-comment': 'hello there #woo'},
                                    follow=True)

        self.assertEqual(response.status_code, 200,
                         "Posting dweet return 200. Status code " + str(response.status_code))

        dweet = Dweet.objects.get(code='test_code')
        self.assertEqual(dweet.code, 'test_code')
        self.assertEqual(dweet.author, user)
        self.assertEqual(dweet.reply_to, self.dweet)

        comment = Comment.objects.get(reply_to=dweet)
        self.assertEqual(comment.text, 'hello there #woo')
        self.assertEqual(comment.author, user)

        hashtag = Hashtag.objects.get(name='woo')
        self.assertEqual(dweet in hashtag.dweets.all(), True)

    def test_too_long_dweet_reply(self):
        user = self.login()

        response = self.client.post('/d/1000/reply', {'code': 'test code that is way too long,' +
                                                      'wow this looks long in code.' +
                                                      'We could fit so much in here.' +
                                                      'oh wow. mooooooooooooooooar text.' +
                                                      'Getting there.' +
                                                      'And BAM tooo long!'}, follow=True)
        self.assertContains(response, "Dweet code too long!", status_code=400)

        # shorter code should go through!
        response = self.client.post('/d/1000/reply', {'code': 'test code that is a lot shorter,' +
                                                      'wow this looks long in code.' +
                                                      'And BAM not tooo long!'}, follow=True)
        self.assertEqual(response.status_code, 200)

        dweets = Dweet.objects.filter(author=user)
        self.assertEqual(dweets.count(), 2)

    def test_like_dweet(self):
        pass  # TODO

    def test_unlike_dweet(self):
        pass  # TODO

    def test_delete_dweet(self):
        pass  # TODO

    def test_GET_requests_fail(self):
        pass  # TODO
