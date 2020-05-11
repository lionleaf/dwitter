import random
from django.test import TestCase
from dwitter.feed.views import NewUserFeed, TopUserFeed, HotUserFeed, NewLikedFeed
from dwitter.models import Dweet
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class UserFeedTestCase():  # Not inheriting from TestCase, an abstract test class if you will
    request_factory = RequestFactory()

    def setUp(self):
        self.users = []
        for i in range(10):
            self.users.append(User.objects.create(username="arrayuser" + str(i), password=""))

        now = timezone.now()

        d_id = 0
        dweets = []
        for user in self.users:
            for i in range(10):
                dweets.append(Dweet.objects.create(id=d_id,
                                                   code="filler "+str(i),
                                                   posted=now - timedelta(minutes=i),
                                                   author=user))
                d_id += 1
                random.seed(1337)
                # add random likes between 0 and 5
                for i in range(random.randrange(0, 5)):
                    dweets[-1].likes.add(self.users[i])

        # Guarantee that all users have at least two liked dweets
        for i in range(10):
            dweets[0].likes.add(self.users[i])
            dweets[2].likes.add(self.users[i])

    def test_all_dweet_author(self):
        self.dweetFeed.kwargs = {'url_username': self.users[3].username}
        queryset = self.dweetFeed.get_queryset()
        for dweet in queryset:
            self.assertEqual(self.users[3], dweet.author)

    def test_queryset_size(self):
        self.dweetFeed.kwargs = {'url_username': self.users[1].username}
        queryset = self.dweetFeed.get_queryset()
        # Each user have 10 dweets from setUp
        self.assertEqual(queryset.count(), 10)


class NewUserFeedTests(UserFeedTestCase, TestCase):
    dweetFeed = NewUserFeed()


class TopUserFeedTests(UserFeedTestCase, TestCase):
    dweetFeed = TopUserFeed()

    def test_annotation(self):
        self.dweetFeed.kwargs = {'url_username': self.users[1].username}
        queryset = self.dweetFeed.get_queryset()
        for dweet in queryset:
            try:
                num_likes = dweet.num_likes
                self.assertEqual(num_likes, dweet.likes.count())
            except:
                self.fail("queryset missing num_likes annotation")


class HotUserFeedTests(UserFeedTestCase, TestCase):
    dweetFeed = HotUserFeed()


class NewLikedFeedTests(UserFeedTestCase, TestCase):
    dweetFeed = NewLikedFeed()

    def test_queryset_objects(self):
        self.dweetFeed.kwargs = {'url_username': self.users[3].username}
        queryset = self.dweetFeed.get_queryset()
        for dweet in queryset:
            self.assertIn(self.users[3], dweet.likes.all())

    def test_all_dweet_author(self):
        pass

    def test_queryset_size(self):
        pass
