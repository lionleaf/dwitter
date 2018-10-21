from django.conf import settings
from django.urls import reverse
import json
import urllib2


class Webhooks:
    @staticmethod
    def send_discord_message(message):
        if(not hasattr(settings, 'DISCORD_WEBHOOK')):
            return  # No discord webhook set up
        post_data = {'content': message}

        # A User-Agent string is required, so I'm just making one up
        req = urllib2.Request(settings.DISCORD_WEBHOOK, json.dumps(post_data),
                              {'Content-Type': 'application/json', 'User-Agent': 'Dwitter/1.0'})
        try:
            f = urllib2.urlopen(req)
            f.close()
        except Exception:
            return  # Fail silently, webhooks will stop rather than breaking the site

    @staticmethod
    def new_dweet_notifications(dweet):
        authorname = dweet.author.username
        msg = ('[u/%s](https://www.dwitter.net%s) posted new dweet ' %
               (authorname, reverse('user_feed', args=[authorname])) +
               '[d/%d](https://www.dwitter.net%s):\n```js\n%s\n```' %
               (dweet.id, reverse('dweet_show', args=[dweet.id]), dweet.code))

        Webhooks.send_discord_message(msg)
