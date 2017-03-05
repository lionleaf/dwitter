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

    def test_dweet_reply_to_set_deleted_field_on_delete(self):
        dweet1 = Dweet.objects.get(id=1)
        dweet1.delete()
        self.assertEqual(dweet1.deleted, True)
        self.assertEqual(Dweet.objects.get(id=2).reply_to, dweet1)

    def test_dweet_author_set_null_on_delete(self):
        User.objects.get(username="user1").delete()
        self.assertTrue(Dweet.with_deleted.get(id=1).deleted)
        self.assertIsNotNone(Dweet.objects.get(id=2).author)

    def test_dweet_has_correct_likes(self):
        dweet1 = Dweet.objects.get(id=1)
        dweet2 = Dweet.objects.get(id=2)
        all_users = [repr(u) for u in User.objects.all()]

        self.assertQuerysetEqual(dweet1.likes.all(), [])
        self.assertQuerysetEqual(dweet2.likes.order_by('id'), all_users)

    def test_default_manager_does_not_include_deleted_dweets(self):
        second_dweet = [repr(Dweet.objects.get(id=2))]
        Dweet.objects.get(id=1).delete()
        self.assertQuerysetEqual(Dweet.objects.all(), second_dweet)

    def test_with_deleted_manager_includes_deleted_dweets(self):
        all_dweets = [repr(d) for d in Dweet.objects.all()]
        Dweet.objects.get(id=1).delete()
        self.assertQuerysetEqual(Dweet.with_deleted.all(), all_dweets)
