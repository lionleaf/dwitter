import random
from django.test import TestCase
from dwitter.feed.views import NewDweetFeed, RandomDweetFeed, HotDweetFeed, DweetFeed
from dwitter.feed.views import TopWeekDweetFeed, TopMonthDweetFeed
from dwitter.feed.views import TopYearDweetFeed, TopAllDweetFeed
from dwitter.models import Comment, Dweet
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class DweetFeedMixin:  # Not inheriting from TestCase, an abstract test class if you will
    request_factory = RequestFactory()

    def setUp(self):
        self.nr_dweets = 15

        users = []
        for i in range(10):
            users.append(User.objects.create(username="arrayuser" + str(i), password=""))

        now = timezone.now()

        # Old dweet with the highest amount of likes should be top of /top/all
        self.top_old_dweet = Dweet.objects.create(id=1,
                                                  code="top alltime",
                                                  posted=now - timedelta(days=1000),
                                                  author=users[0])

        # add 10 likes
        for i in range(10):
            self.top_old_dweet.likes.add(users[i])

        # Almost year-old dweet with the highest amount of likes should be top of /top
        self.top_year_dweet = Dweet.objects.create(id=10233,
                                                   code="top yr",
                                                   posted=now - timedelta(days=200),
                                                   author=users[0])
        # add 8 likes
        for i in range(9):
            self.top_year_dweet.likes.add(users[i])

        self.top_month_dweet = Dweet.objects.create(id=13232,
                                                    code="top month",
                                                    posted=now - timedelta(days=20),
                                                    author=users[0])
        # add 8 likes
        for i in range(8):
            self.top_month_dweet.likes.add(users[i])

        self.top_week_dweet = Dweet.objects.create(id=13209,
                                                   code="top week",
                                                   posted=now - timedelta(days=5),
                                                   author=users[0])
        # add 8 likes
        for i in range(7):
            self.top_week_dweet.likes.add(users[i])

        # Popular dweet, should be top of /hot, but not /top
        self.hottest_dweet = Dweet.objects.create(id=3,
                                                  code="popular",
                                                  posted=now - timedelta(minutes=2),
                                                  reply_to=self.top_old_dweet,
                                                  author=users[2])
        # add 7 likes
        for i in range(6):
            self.hottest_dweet.likes.add(users[i])

        for i in range(10):
            filler_dweet = Dweet.objects.create(id=1000+i,
                                                code="filler "+str(i),
                                                posted=now - timedelta(minutes=i),
                                                author=users[i])
            random.seed(1337)
            # add random likes between 0 and 5
            for i in range(random.randrange(0, 5)):
                filler_dweet.likes.add(users[i])

        # Add comments with some #hashtags
        Comment.objects.create(id=1,
                               text="comment1 text with #hashtag #test ",
                               posted=now - timedelta(minutes=1),
                               reply_to=self.top_old_dweet,
                               author=users[1])

        Comment.objects.create(id=2,
                               text="comment2 text #hashtag #test #hash1",
                               posted=now,
                               reply_to=self.hottest_dweet,
                               author=users[2])

    def test_queryset_count(self):
        queryset = self.dweetFeed.get_queryset()
        self.assertEqual(queryset.count(), self.nr_dweets)

    def test_no_default_title(self):
        title = self.dweetFeed.title
        self.assertNotEqual(DweetFeed().title, title, "Each feed should have a unique title")

    def test_html_response(self):
        request = self.request_factory.get('/')
        request.session = {}
        response = self.dweetFeed.__class__.as_view()(request)
        response.render()
        html = response.content.decode('utf8')
        self.assertIn('<title>' + self.dweetFeed.title + '</title>', html)


class TopFeedTestMixin:
    def test_annotation(self):
        queryset = self.dweetFeed.get_queryset()
        for dweet in queryset:
            try:
                num_likes = dweet.num_likes
                self.assertTrue(num_likes >= 0)
            except:
                self.fail("queryset missing num_likes annotation")


class HotDweetFeedTests(DweetFeedMixin, TestCase):
    dweetFeed = HotDweetFeed()

    def test_hot_sort(self):
        queryset = self.dweetFeed.get_queryset()
        first_dweet = queryset.first()
        prev_hotness = first_dweet.hotness
        self.assertEqual(first_dweet, self.hottest_dweet)
        for dweet in queryset:
            self.assertTrue(prev_hotness >= dweet.hotness, "Should be sorted by hotness")
            prev_hotness = dweet.hotness


class TopWeekDweetFeedTests(DweetFeedMixin, TopFeedTestMixin, TestCase):
    dweetFeed = TopWeekDweetFeed()

    def test_top_sort(self):
        queryset = self.dweetFeed.get_queryset()

        first_dweet = queryset.first()
        self.assertEqual(first_dweet, self.top_week_dweet)

        prev_score = first_dweet.num_likes
        for dweet in queryset:
            self.assertTrue(prev_score >= dweet.num_likes, "Should sort by num likes")
            prev_score = dweet.num_likes

    def test_queryset_count(self):
        """ Override test, since certain older dweets are skipped """
        queryset = self.dweetFeed.get_queryset()
        self.assertEqual(queryset.count(), self.nr_dweets - 3)


class TopMonthDweetFeedTests(DweetFeedMixin, TopFeedTestMixin, TestCase):
    dweetFeed = TopMonthDweetFeed()

    def test_top_sort(self):
        queryset = self.dweetFeed.get_queryset()

        first_dweet = queryset.first()
        self.assertEqual(first_dweet, self.top_month_dweet)

        prev_score = first_dweet.num_likes
        for dweet in queryset:
            self.assertTrue(prev_score >= dweet.num_likes, "Should sort by num likes")
            prev_score = dweet.num_likes

    def test_queryset_count(self):
        """ Override test, since certain older dweets are skipped """
        queryset = self.dweetFeed.get_queryset()
        self.assertEqual(queryset.count(), self.nr_dweets - 2)


class TopYearDweetFeedTests(DweetFeedMixin, TopFeedTestMixin, TestCase):
    dweetFeed = TopYearDweetFeed()

    def test_top_sort(self):
        queryset = self.dweetFeed.get_queryset()

        first_dweet = queryset.first()
        self.assertEqual(first_dweet, self.top_year_dweet)

        prev_score = first_dweet.num_likes
        for dweet in queryset:
            self.assertTrue(prev_score >= dweet.num_likes, "Should sort by num likes")
            prev_score = dweet.num_likes

    def test_queryset_count(self):
        """ Override test, since certain older dweets are skipped """
        queryset = self.dweetFeed.get_queryset()
        self.assertEqual(queryset.count(), self.nr_dweets - 1)


class TopAllDweetFeedTests(DweetFeedMixin, TopFeedTestMixin, TestCase):
    dweetFeed = TopAllDweetFeed()

    def test_top_sort(self):
        queryset = self.dweetFeed.get_queryset()

        first_dweet = queryset.first()
        self.assertEqual(first_dweet, self.top_old_dweet)

        prev_score = first_dweet.num_likes
        for dweet in queryset:
            self.assertTrue(prev_score >= dweet.num_likes, "Should sort by num likes")
            prev_score = dweet.num_likes


class NewDweetFeedTests(DweetFeedMixin, TestCase):
    dweetFeed = NewDweetFeed()

    def test_new_sort(self):
        queryset = self.dweetFeed.get_queryset()
        first_dweet = queryset.first()
        prev_date = first_dweet.posted
        for dweet in queryset:
            self.assertTrue(prev_date >= dweet.posted, "Should sort by date")
            prev_date = dweet.posted


class RandomDweetFeedTests(DweetFeedMixin, TestCase):
    dweetFeed = RandomDweetFeed()
