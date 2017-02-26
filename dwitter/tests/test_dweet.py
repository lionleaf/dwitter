from django.test import TestCase
from django.contrib.auth.models import User
from dwitter.models import Dweet
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
        dweet2.likes.add(user1, user2)

    def test_dweet_renders_to_string_correctly(self):
        self.assertEqual(Dweet.objects.get(id=1).__unicode__(), "d/1 (user1)")
        self.assertEqual(Dweet.objects.get(id=2).__unicode__(), "d/2 (user2)")

    def test_dweet_reply_to_set_null_on_delete(self):
        Dweet.objects.get(id=1).delete()
        self.assertEqual(Dweet.objects.get(id=2).reply_to, None)

    def test_dweet_author_cascade_on_delete(self):
        User.objects.get(username="user1").delete()
        with self.assertRaises(Dweet.DoesNotExist):
            Dweet.objects.get(id=1)
        Dweet.objects.get(id=2)

    def test_dweet_has_correct_likes(self):
        self.assertEqual(Dweet.objects.get(id=1).likes.count(), 0)

        dweet2 = Dweet.objects.get(id=2)
        self.assertEqual(dweet2.likes.count(), 2)
        self.assertIn(User.objects.get(username="user1"), dweet2.likes.all())
        self.assertIn(User.objects.get(username="user2"), dweet2.likes.all())
