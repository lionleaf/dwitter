from django.conf import settings
import requests


class Webhooks:
    @staticmethod
    def send_discord_message(message):
        if(not hasattr(settings, 'DISCORD_WEBHOOK')):
            return  # No discord webhook set up

        post_data = {'content': message}

        try:
            requests.post(settings.DISCORD_WEBHOOK, json=post_data)
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
