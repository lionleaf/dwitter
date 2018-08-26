from django.test import TestCase
from django.contrib.auth.models import User
from dwitter.models import Dweet
from dwitter.models import Comment
from django.utils import timezone
from datetime import timedelta


class DweetTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1", password="")
        user2 = User.objects.create(username="user2", password="")

        now = timezone.now()

        dweet1 = Dweet.objects.create(id=1,
                                      code="dweet1 code",
                                      posted=now - timedelta(minutes=1),
                                      author=user1)

        dweet2 = Dweet.objects.create(id=2,
                                      code="dweet2 code",
                                      posted=now,
                                      reply_to=dweet1,
                                      author=user2)

        Comment.objects.create(id=1,
                               text="comment1 text",
                               posted=now - timedelta(minutes=1),
                               reply_to=dweet2,
                               author=user1)

        Comment.objects.create(id=2,
                               text="comment2 text",
                               posted=now,
                               reply_to=dweet1,
                               author=user2)

    def test_comment_renders_to_string_correctly(self):
        self.assertEqual(Comment.objects.get(id=1).__str__(),
                         "c/1 (user1) to d/2 (user2)")
        self.assertEqual(Comment.objects.get(id=2).__str__(),
                         "c/2 (user2) to d/1 (user1)")

    def test_comment_reply_to_do_nothing_on_soft_delete(self):
        Dweet.objects.get(id=2).delete()
        self.assertTrue(Comment.objects.get(id=1).reply_to.deleted)
        self.assertEqual(Comment.objects.get(id=2).reply_to,
                         Dweet.objects.get(id=1))

    def test_comment_author_cascade_on_delete(self):
        User.objects.get(username="user1").delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=1)
        self.assertEqual(Comment.objects.get(id=2).author,
                         User.objects.get(id=2))
