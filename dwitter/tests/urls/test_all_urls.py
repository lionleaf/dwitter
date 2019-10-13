from django import test
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from dwitter.models import Dweet, Comment
from django.utils import timezone
from datetime import timedelta
import importlib
from django.contrib import auth


# Some automatic based on
# https://stackoverflow.com/questions/14454001/list-all-suburls-and-check-if-broken-in-python
class UrlsTest(test.TestCase):

    def setUp(self):
        user1 = User.objects.create(username="user1", password="qwertypw")
        user1.set_password('qwertypw')  # Properly hash the password
        user1.save()

        user2 = User.objects.create(username="user2", password="qwertypw")
        user2.set_password('qwertypw')  # Properly hash the password
        user2.save()

        now = timezone.now()

        dweet1 = Dweet.objects.create(id=1,
                                      code="dweet1 code",
                                      posted=now - timedelta(hours=1),
                                      author=user1)

        dweet2 = Dweet.objects.create(id=2,
                                      code="dweet2 code",
                                      posted=now,
                                      reply_to=dweet1,
                                      author=user2)

        dweet2.likes.add(user1, user2)

        Comment.objects.create(id=1,
                               text="comment1 text with #hashtag #test #2hash",
                               posted=now - timedelta(minutes=1),
                               reply_to=dweet2,
                               author=user1)

        Comment.objects.create(id=2,
                               text="comment2 text #hashtag #1hash #hash1",
                               posted=now,
                               reply_to=dweet1,
                               author=user2)

        def test_logged_in_urls(self):
            self.responses_test(credentials={'username': 'user1', 'password': 'qwertypw'})

    def test_guest_urls(self):
        self.responses_test(allowed_http_codes=[200, 302, 403, 405], credentials={})

    def responses_test(self, allowed_http_codes=[200, 302, 405], logout_url="logout", quiet=False,
                       credentials={},
                       default_kwargs={'username': 'user1',
                                       'url_username': 'user1',
                                       'sort': 'new',
                                       'dweet_id': '2',
                                       'hashtag_name': 'test'}):
        """
        Test all pattern in root urlconf and included ones.
        Do GET requests only.
        A pattern is skipped if any of the conditions applies:
            - pattern has no name in urlconf
            - pattern expects any positinal parameters
            - pattern expects keyword parameters that are not specified in @default_kwargs
        If response code is not in @allowed_http_codes, fail the test.
        if @credentials dict is specified (e.g. username and password),
            login before run tests.
        If @logout_url is specified, then check if we accidentally logged out
            the client while testing, and login again
        Specify @default_kwargs to be used for patterns that expect keyword parameters,
            e.g. if you specify default_kwargs={'username': 'testuser'}, then
            for pattern url(r'^accounts/(?P<username>[\.\w-]+)/$'
            the url /accounts/testuser/ will be tested.
        If @quiet=False, print all the urls checked. If status code of the response is not 200,
            print the status code.
        """
        module = importlib.import_module(settings.ROOT_URLCONF)
        print(credentials)
        if credentials:
            self.client.login(**credentials)
            user = auth.get_user(self.client)
            assert user.is_authenticated

        def check_urls(urlpatterns, prefix=''):
            for pattern in urlpatterns:
                if hasattr(pattern, 'url_patterns'):
                    # this is an included urlconf
                    new_prefix = prefix
                    if pattern.namespace:
                        new_prefix = prefix + (":" if prefix else "") + pattern.namespace
                    check_urls(pattern.url_patterns, prefix=new_prefix)
                params = {}
                skip = False
                regex = pattern.pattern.regex
                if regex.groups > 0:
                    # the url expects parameters
                    # use default_kwargs supplied
                    if regex.groups > len(regex.groupindex.keys()) \
                            or set(regex.groupindex.keys()) - set(default_kwargs.keys()):
                        # there are positional parameters OR
                        # keyword parameters that are not supplied in default_kwargs
                        # so we skip the url
                        skip = True
                    else:
                        for key in set(default_kwargs.keys()) & set(regex.groupindex.keys()):
                            params[key] = default_kwargs[key]
                if hasattr(pattern, "name") and pattern.name:
                    name = pattern.name
                else:
                    # if pattern has no name, skip it
                    skip = True
                    name = ""
                fullname = (prefix + ":" + name) if prefix else name
                if not skip:
                    url = reverse(fullname, kwargs=params)
                    response = self.client.get(url)
                    self.assertIn(response.status_code, allowed_http_codes,
                                  "Invalid status: " + str(response.status_code) + " for " + url)
                    # print status code if it is not 200
                    status = "" if response.status_code == 200 else str(response.status_code) + " "
                    if not quiet:
                        print(status + url)
                    if logout_url in url and credentials:
                        # if we just tested logout, then login again
                        self.client.login(**credentials)
                else:
                    if not quiet:
                        print("SKIP " + regex.pattern + " " + fullname)
        check_urls(module.urlpatterns)
