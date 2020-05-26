from django.test import TestCase
from django.contrib.auth.models import User
from dwitter.models import Dweet, DweetNotification, Comment
from django.utils import timezone
from datetime import timedelta

class DweetNotificationTestCase(TestCase):
    def setUp(self):
        self.alice = User.objects.create(username="alice", password="")
        self.bob = User.objects.create(username="bob", password="")
        self.carol = User.objects.create(username="carol", password="")
        self.doug = User.objects.create(username="doug", password="")

        self.now = timezone.now()

        self.alicedweet = Dweet.objects.create(id=1,
                                      code="alicedweet code",
                                      posted=self.now - timedelta(minutes=1),
                                      author=self.alice)

    def test_like_notification_to_author(self):
        self.alicedweet.likes.add(self.bob)

        self.assertEqual(DweetNotification.objects.all().count(),1)

        notification = DweetNotification.objects.all()[0]
        self.assertEqual(notification.verb, "like")
        self.assertEqual(notification.recipient, self.alice)


    def test_no_notification_for_self_like(self):
        self.alicedweet.likes.add(self.alice)
        self.assertEqual(DweetNotification.objects.all().count(),0)


    def test_comment_notification_to_author(self):
        Comment.objects.create(id=1,
                               text="comment1 text",
                               reply_to=self.alicedweet,
                               author=self.bob)

        self.assertEqual(DweetNotification.objects.all().count(),1)

        notification = DweetNotification.objects.all()[0]
        self.assertEqual(notification.verb, "comment")
        self.assertEqual(notification.recipient, self.alice)


    def test_no_notification_for_self_comment(self):
        Comment.objects.create(id=1,
                               text="comment1 text",
                               reply_to=self.alicedweet,
                               author=self.alice)

        self.assertEqual(DweetNotification.objects.all().count(),0)


    def test_notification_for_comment_on_commented_dweet(self):
        """ Bob comments on Alice's dweet, then Alice comments.
            Bob shold get a notificaiton
            """ 

        # Bob comments
        Comment.objects.create(id=1,
                               text="Nice dweet Alice",
                               reply_to=self.alicedweet,
                               author=self.bob)

        self.assertEqual(DweetNotification.objects.all().count(), 1)

        # Alice replies
        Comment.objects.create(id=2,
                               text="Thanks, Bob!",
                               reply_to=self.alicedweet,
                               author=self.alice)

        self.assertEqual(DweetNotification.objects.filter().count(), 2)
        self.assertEqual(DweetNotification.objects.filter(recipient=self.bob).count(), 1)


    def test_remix_notification_to_author(self):
        bobremix = Dweet.objects.create(id=2,
                                      code="bob is cool",
                                      reply_to=self.alicedweet,
                                      author=self.bob)

        self.assertEqual(DweetNotification.objects.all().count(),1)

        notification = DweetNotification.objects.all()[0]
        self.assertEqual(notification.verb, "remix")
        self.assertEqual(notification.actors.all()[0], self.bob)
        self.assertEqual(notification.recipient, self.alice)


    def test_comment_notification_no_duplication(self):
        # Alice likes her own dweet
        self.alicedweet.likes.add(self.alice)

        # Alice comments on her own dweet
        Comment.objects.create(text="My dweet is awaesom",
                               reply_to=self.alicedweet,
                               author=self.alice)

        # No notifications yet
        self.assertEqual(DweetNotification.objects.all().count(), 0)

        # Bob comments twice
        Comment.objects.create(text="Great one",
                               reply_to=self.alicedweet,
                               author=self.bob)
        Comment.objects.create(text="Wait until you see my remix!",
                               reply_to=self.alicedweet,
                               author=self.bob)

        # Carol comments
        Comment.objects.create(text="I agree with Bob, it's a masterpiece",
                               reply_to=self.alicedweet,
                               author=self.carol)

        #Single notification to Alice and Bob
        self.assertEqual(DweetNotification.objects.all().count(), 2)
        self.assertEqual(DweetNotification.objects.filter(recipient=self.alice).count(), 1)
        self.assertEqual(DweetNotification.objects.filter(recipient=self.bob).count(), 1)

        notification = DweetNotification.objects.filter(recipient=self.alice).all()[0]
        self.assertEqual(notification.verb, "comment")
        self.assertEqual(notification.actors.all()[0], self.bob)
        self.assertEqual(notification.actors.all()[1], self.carol)

        notification = DweetNotification.objects.filter(recipient=self.bob).all()[0]
        self.assertEqual(notification.actors.all().count(), 1) 
        self.assertEqual(notification.actors.all()[0], self.carol) 


    def test_accumulated_like_notification(self):
        # Bob and Carol likes Alice's dweet
        self.alicedweet.likes.add(self.bob)
        self.alicedweet.likes.add(self.carol)

        # Alice should see a single coalesced notification
        self.assertEqual(DweetNotification.objects.all().count(), 1)
        notification = DweetNotification.objects.all()[0]
        self.assertEqual(notification.actors.count(), 2)  # Bob and Carol

        # Alice reads the notification
        notification.read = True
        notification.save()

        # Then Doug likes it
        self.alicedweet.likes.add(self.doug)

        # Should result in a new notification
        self.assertEqual(DweetNotification.objects.all().count(), 2)

        return


    def test_accumulated_comment_notification(self):
        # Bob and Carol likes Alice's dweet
        Comment.objects.create(text="Beautiful!",
                               reply_to=self.alicedweet,
                               author=self.bob)
        Comment.objects.create(text="Stunning!",
                               reply_to=self.alicedweet,
                               author=self.carol)

        # Alice and Bob should see one notification each, but Alice should have 2 actors
        self.assertEqual(DweetNotification.objects.all().count(), 2)

        alice_notification = DweetNotification.objects.filter(recipient=self.alice)[0]
        bob_notification = DweetNotification.objects.filter(recipient=self.bob)[0]

        self.assertEqual(alice_notification.actors.count(), 2)  # Bob and Carol
        self.assertEqual(bob_notification.actors.count(), 1)  # Only Carol

        # Alice reads the notification
        alice_notification.read = True
        alice_notification.save()

        # Then Doug comments
        Comment.objects.create(text="Magic",
                               reply_to=self.alicedweet,
                               author=self.doug)

        # Should result in a new notification for Alice but accumulated for Bob and fresh for Carol
        self.assertEqual(DweetNotification.objects.all().count(), 4)

        self.assertEqual(DweetNotification.objects.filter(recipient=self.alice).count(), 2)
        self.assertEqual(DweetNotification.objects.filter(recipient=self.bob).count(), 1)
        self.assertEqual(DweetNotification.objects.filter(recipient=self.carol).count(), 1)


    def test_remix_notifications_not_accumulating(self):
        # Bob and Carol likes Alice's dweet
        Dweet.objects.create(id=2,
                code="bob is cool",
                reply_to=self.alicedweet,
                author=self.bob)

        Dweet.objects.create(id=3,
                code="alicerrrremix",
                reply_to=self.alicedweet,
                author=self.carol)

        # Alice should get two notifications
        self.assertEqual(DweetNotification.objects.all().count(), 2)
        self.assertEqual(DweetNotification.objects.filter(recipient=self.alice).count(), 2)

