from django.conf import settings
import json
# Support for python3 and 2.7
from future.standard_library import install_aliases
install_aliases()
from urllib.request import urlopen, Request  # noqa: E402


class Webhooks:
    @staticmethod
    def send_discord_message(message):
        if(not hasattr(settings, 'DISCORD_WEBHOOK')):
            return  # No discord webhook set up
        post_data = {'content': message}

        # A User-Agent string is required, so I'm just making one up
        req = Request(settings.DISCORD_WEBHOOK, json.dumps(post_data),
                      {'Content-Type': 'application/json', 'User-Agent': 'Dwitter/1.0'})
        try:
            f = urlopen(req)
            f.close()
        except Exception:
            return  # Fail silently, webhooks will stop rather than breaking the site

    @staticmethod
    def new_dweet_notifications(dweet):
        authorname = dweet.author.username
        msg = ('[u/%s](https://www.dwitter.net/u/%s) posted new dweet ' %
               (authorname, authorname) +
               '[d/%d](https://www.dwitter.net/d/%s):\n```js\n%s\n```' %
               (dweet.id, dweet.id, dweet.code))

        Webhooks.send_discord_message(msg)
