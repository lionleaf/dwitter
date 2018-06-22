import random
from django.test import TestCase
from dwitter.feed.views import NewDweetFeed, TopDweetFeed, RandomDweetFeed, HotDweetFeed, DweetFeed
from django.contrib.auth.models import User
from dwitter.models import Dweet
from django.utils import timezone
from datetime import timedelta


class DweetFeedTestCase():  # Not inheriting from TestCase, an abstract test class if you will

    def setUp(self):
        self.nr_dweets = 12

        users = []
        for i in range(10):
            users.append(User.objects.create(username="arrayuser" + str(i), password=""))

        now = timezone.now()

        # Old dweet with the highest amount of likes should be top of /top
        self.top_old_dweet = Dweet.objects.create(id=1,
                                                  code="top code",
                                                  posted=now - timedelta(days=35),
                                                  author=users[0])
        # add 10 likes
        for i in range(10):
            self.top_old_dweet.likes.add(users[i])

        # Popular dweet, should be top of /hot, but not /top
        self.hottest_dweet = Dweet.objects.create(id=3,
                                                  code="popular",
                                                  posted=now - timedelta(minutes=2),
                                                  reply_to=self.top_old_dweet,
                                                  author=users[2])
        # add 7 likes
        for i in range(7):
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

    def test_annotation(self):
        queryset = self.dweetFeed.get_queryset()
        for dweet in queryset:
            try:
                num_likes = dweet.num_likes
                self.assertTrue(num_likes >= 0)
            except:
                self.fail("queryset missing num_likes annotation")

    def test_queryset_count(self):
        queryset = self.dweetFeed.get_queryset()
        self.assertEqual(queryset.count(), self.nr_dweets)

    def test_no_default_title(self):
        title = self.dweetFeed.title
        self.assertNotEqual(DweetFeed().title, title, "Each feed should have a unique title")


class HotDweetFeedTests(DweetFeedTestCase, TestCase):
    dweetFeed = HotDweetFeed()

    def test_hot_sort(self):
        queryset = self.dweetFeed.get_queryset()
        first_dweet = queryset.first()
        prev_hotness = first_dweet.hotness
        self.assertEqual(first_dweet, self.hottest_dweet)
        for dweet in queryset:
            self.assertTrue(prev_hotness >= dweet.hotness, "Should be sorted by hotness")
            prev_hotness = dweet.hotness


class TopDweetFeedTests(DweetFeedTestCase, TestCase):
    dweetFeed = TopDweetFeed()

    def test_top_sort(self):
        queryset = self.dweetFeed.get_queryset()
        first_dweet = queryset.first()
        prev_score = first_dweet.num_likes
        self.assertEqual(first_dweet, self.top_old_dweet)
        for dweet in queryset:
            self.assertTrue(prev_score >= dweet.num_likes, "Should sort by num likes")
            prev_score = dweet.num_likes


class NewDweetFeedTests(DweetFeedTestCase, TestCase):
    dweetFeed = NewDweetFeed()

    def test_new_sort(self):
        queryset = self.dweetFeed.get_queryset()
        first_dweet = queryset.first()
        prev_date = first_dweet.posted
        for dweet in queryset:
            self.assertTrue(prev_date >= dweet.posted, "Should sort by date")
            prev_date = dweet.posted


class RandomDweetFeedTests(DweetFeedTestCase, TestCase):
    dweetFeed = RandomDweetFeed()
