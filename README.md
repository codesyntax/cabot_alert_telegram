Cabot Telegram Plulgin
=====

Based on: https://github.com/lblasc/cabot-alert-slack

This is an alert plugin for the cabot service monitoring tool. It allows you to alert users using a Telegram chat room.

## Installation

Enter the cabot virtual environment.
```
    $ pip install cabot_alert_telegram
    $ foreman stop
```

or

```
    $ pip install git+git://github.com/codesyntax/cabot_alert_telegram.git
    $ foreman stop
```

Edit `conf/*.env`.

```
CABOT_PLUGINS_ENABLED=cabot_alert_telegram=0.1
...
TELEGRAM_BOT_TOKEN=bot_token
TELEGRAM_CHAT_ID=id of the chat where messages will be sent
```

Add cabot_alert_telegram to the installed apps in settings.py
```
    $ foreman run python manage.py syncdb
    $ foreman start
```
