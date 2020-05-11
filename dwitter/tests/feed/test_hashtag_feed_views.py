import random
from django.http import Http404
from django.test import TestCase
from dwitter.feed.views import NewHashtagFeed, TopHashtagFeed
from dwitter.models import Comment, Dweet
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class HashtagFeedTestCase():  # Not inheriting from TestCase, an abstract test class if you will
    request_factory = RequestFactory()
    dweetFeed = {}

    def setUp(self):
        users = []
        for i in range(10):
            users.append(User.objects.create(username="arrayuser" + str(i), password=""))

        now = timezone.now()

        dweets = []
        for i in range(10):
            dweets.append(Dweet.objects.create(id=1000+i,
                                               code="filler "+str(i),
                                               posted=now - timedelta(minutes=i),
                                               author=users[i]))

            # Add comments with some #hashtags
            Comment.objects.create(id=1+i,
                                   text="#everyone #has #this #hashtag",
                                   posted=now - timedelta(minutes=i-1),
                                   reply_to=dweets[i],
                                   author=users[0])

            random.seed(1337)
            # add random likes between 0 and 9
            for like in range(random.randrange(0, 9)):
                dweets[i].likes.add(users[like])

        Comment.objects.create(id=2432,
                               text="#Special #comment #hashtag #hash1",
                               posted=now,
                               reply_to=dweets[3],
                               author=users[2])

    def test_404_empty_hashtag(self):
        request = self.request_factory.get('/')
        request.session = {}
        with self.assertRaises(Http404):
            self.dweetFeed.__class__.as_view()(request, hashtag_name='empty')

    def test_queryset_count(self):
        self.dweetFeed.kwargs = {'hashtag_name': 'everyone'}
        queryset = self.dweetFeed.get_queryset()
        self.assertEqual(queryset.count(), 10)

        self.dweetFeed.kwargs = {'hashtag_name': 'special'}
        queryset = self.dweetFeed.get_queryset()
        self.assertEqual(queryset.count(), 1)

    def test_no_default_title(self):
        request = self.request_factory.get('/')
        request.session = {}
        response = self.dweetFeed.__class__.as_view()(request, hashtag_name='everyone')
        response.render()
        html = response.content.decode('utf8')
        self.assertNotIn('<title>' + self.dweetFeed.title + '</title>', html)

    def test_got_title(self):
        self.dweetFeed.kwargs = {'hashtag_name': 'everyone'}
        request = self.request_factory.get('/')
        request.session = {}
        response = self.dweetFeed.__class__.as_view()(request, hashtag_name='everyone')
        response.render()
        html = response.content.decode('utf8')
        self.assertIn('<title>' + self.dweetFeed.get_title() + '</title>', html)

    def test_html_response(self):
        request = self.request_factory.get('/')
        request.session = {}
        response = self.dweetFeed.__class__.as_view()(request, hashtag_name='everyone')
        response.render()
        html = response.content.decode('utf8')
        self.assertIn('<title>', html)


class TopHashtagFeedTests(HashtagFeedTestCase, TestCase):
    dweetFeed = TopHashtagFeed()

    def test_top_sort(self):
        self.dweetFeed.kwargs = {'hashtag_name': 'everyone'}
        queryset = self.dweetFeed.get_queryset()
        first_dweet = queryset.first()
        prev_score = first_dweet.num_likes
        for dweet in queryset:
            self.assertTrue(prev_score >= dweet.num_likes, "Should sort by num likes")
            prev_score = dweet.num_likes

    def test_annotation(self):
        self.dweetFeed.kwargs = {'hashtag_name': 'everyone'}
        queryset = self.dweetFeed.get_queryset()
        for dweet in queryset:
            try:
                num_likes = dweet.num_likes
                self.assertTrue(num_likes >= 0)
            except:
                self.fail("queryset missing num_likes annotation")


class NewHashtagFeedTests(HashtagFeedTestCase, TestCase):
    dweetFeed = NewHashtagFeed()

    def test_new_sort(self):
        self.dweetFeed.kwargs = {'hashtag_name': 'everyone'}
        queryset = self.dweetFeed.get_queryset()
        first_dweet = queryset.first()
        prev_date = first_dweet.posted
        for dweet in queryset:
            self.assertTrue(prev_date >= dweet.posted, "Should sort by date")
            prev_date = dweet.posted
