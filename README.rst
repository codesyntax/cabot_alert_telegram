=====================
Cabot Telegram Plugin
=====================

Based on: https://github.com/lblasc/cabot-alert-slack

This is an alert plugin for the cabot service monitoring tool. It allows you to alert users using a `Telegram`_ chat room.

Installation
==============

Enter the cabot virtual environment::

    $ pip install cabot_alert_telegram
    $ foreman stop


or::


    $ pip install git+git://github.com/codesyntax/cabot_alert_telegram.git
    $ foreman stop


Edit `conf/*.env`::


    CABOT_PLUGINS_ENABLED=cabot_alert_telegram=0.4
    ...
    TELEGRAM_BOT_TOKEN=bot_token
    TELEGRAM_CHAT_ID=id of the chat where messages will be sent


Add cabot_alert_telegram to the installed apps in settings.py::

    $ foreman run python manage.py syncdb
    $ foreman start

Add manually an instance of the Alert Plugin (sometimes it is not added automatically)::

    $ ssh ubuntu@server
    $ source venv/bin/activate
    $ cd cabot
    $ foreman run -e conf/production.env python manage.py shell # point to the correct production.env file
    Python 2.7.3 (default, Dec 18 2014, 19:10:20)
    [GCC 4.6.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> from cabot_alert_telegram.models import TelegramAlert
    >>> ta = TelegramAlert()
    >>> ta.title = u'Telegram'
    >>> ta.save()
    >>> (Ctrl-D to exit)


Telegram Bot
============

You need to create a Telegram bot which will be used to send the messages to the users. To create a new Telegram Bot check the official documentation at https://core.telegram.org/bots

You need to create a new Group Chat, add all your users to that chatroom and add also the Bot there.

To get the chat id, open https://telegram.me and select the group chat you previously created. Check the URL, it will be something like this::

    https://web.telegram.org/#/im?p=g99999999

You need to not the value of p parameter (g99999999) and exchange **g** with a **-**: **-99999999**

This is a bit hacky, but I don't know any other way to get the group id.


.. _Telegram: https://telegram.org
