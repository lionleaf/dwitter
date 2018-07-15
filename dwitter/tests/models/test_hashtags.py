from django.test import TestCase
from django.contrib.auth.models import User
from dwitter.models import Dweet, Comment, Hashtag
from django.utils import timezone
from datetime import timedelta


class HashtagTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1", password="")
        self.user2 = User.objects.create(username="user2", password="")

        now = timezone.now()

        self.dweet1 = Dweet.objects.create(id=1,
                                           code="dweet1 code",
                                           posted=now - timedelta(minutes=1),
                                           author=user1)

        self.dweet2 = Dweet.objects.create(id=2,
                                           code="dweet2 code",
                                           posted=now,
                                           reply_to=self.dweet1,
                                           author=self.user2)

        Comment.objects.create(id=1,
                               text="comment1 text with #hashtag #hash2 #2hash",
                               posted=now - timedelta(minutes=1),
                               reply_to=self.dweet2,
                               author=user1)

        Comment.objects.create(id=2,
                               text="comment2 text #hashtag #1hash #hash1",
                               posted=now,
                               reply_to=self.dweet1,
                               author=self.user2)

    def test_hashtags_created(self):
        h = Hashtag.objects.get(name='hashtag')

        h1 = Hashtag.objects.get(name='hash1')
        h2 = Hashtag.objects.get(name='hash2')

        try:
            illegal1 = Hashtag.objects.get(name='1hash')
            self.assertEqual(illegal1, True)  # should throw an exception!
        except:
            pass

        try:
            illegal2 = Hashtag.objects.get(name='2hash')
            self.assertEqual(illegal2, True)  # should throw an exception!
        except:
            pass

        self.assertEqual(h is None, False)
        self.assertEqual(h1 is None, False)
        self.assertEqual(h2 is None, False)
        self.assertEqual(h.dweets.count(), 2)
        self.assertEqual(h1.dweets.all()[0], self.dweet1)
        self.assertEqual(h2.dweets.all()[0], self.dweet2)

    def test_same_hashtag(self):
        self.dweet3 = Dweet(id=3,
                            code="dweet3 code",
                            posted=timezone.now(),
                            reply_to=None,
                            author=self.user2)
        self.dweet3.save()

        c = Comment(id=3,
                    text="comment3 text #hashtag #h_3 #_3",
                    posted=timezone.now(),
                    reply_to=self.dweet3,
                    author=self.user2)
        c.save()

        h = Hashtag.objects.get(name='hashtag')
        h3 = Hashtag.objects.get(name='h_3')
        h_3 = Hashtag.objects.get(name='_3')
        self.assertEqual(h is None, False)
        self.assertEqual(h3 is None, False)
        self.assertEqual(h_3 is None, False)
        self.assertEqual(h.dweets.count(), 3)
        self.assertEqual(h.dweets.get(id=3), self.dweet3)
        self.assertEqual(h3.dweets.all()[0], self.dweet3)
        self.assertEqual(h_3.dweets.all()[0], self.dweet3)

    def test_no_double_adding(self):
        # add #hashtag and #1hash to dweet1 again and see that the size
        # of those hashtags doesn't change
        Comment.objects.create(id=4,
                               text="comment2 text #hashtag #hash1",
                               posted=timezone.now(),
                               reply_to=self.dweet1,
                               author=self.user2)
        h = Hashtag.objects.get(name='hashtag')
        h1 = Hashtag.objects.get(name='hash1')
        self.assertEqual(h.dweets.count(), 2)
        self.assertEqual(h1.dweets.count(), 1)
