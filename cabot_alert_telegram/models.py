from cabot.cabotapp.alert import AlertPlugin
from cabot.cabotapp.alert import AlertPluginUserData
from django.conf import settings
from django.db import models
from django.template import Context
from django.template import Template
from os import environ as env

import telebot


telegram_template = """{{ service.name }} {% if service.overall_status == service.PASSING_STATUS %}OK{% else %}{{ service.overall_status }}{% endif %}: {{ scheme }}://{{ host }}{% url 'service' pk=service.id %}. {% if service.overall_status != service.PASSING_STATUS %}Checks failing: {% for check in service.all_failing_checks %}{% if check.check_category == 'Jenkins check' %}{% if check.last_result.error %}{{ check.name }} ({{ check.last_result.error|safe }}) {{jenkins_api}}job/{{ check.name }}/{{ check.last_result.job_number }}/console{% else %}{{ check.name }} {{jenkins_api}}/job/{{ check.name }}/{{check.last_result.job_number}}/console{% endif %}{% else %}{{ check.name }}{% if check.last_result.error %} ({{ check.last_result.error|safe }}){% endif %}{% endif %}{% endfor %}{% endif %}{% if alert %}{% for alias in users %}@{{ alias }}{% endfor %}{% endif %}"""

# This provides the telegram alias for each user.
# Each object corresponds to a User


class TelegramAlert(AlertPlugin):
    name = "Telegram"
    author = "Mikel Larreategi"

    def send_alert(self, service, users, duty_officers):
        alert = True
        telegram_aliases = []
        users = list(users) + list(duty_officers)

        telegram_aliases = [u.telegram_id for u in TelegramAlertUserData.objects.filter(user__user__in=users) if u.telegram_id]

        if service.overall_status == service.WARNING_STATUS:
            alert = False  # Don't alert at all for WARNING
        if service.overall_status == service.ERROR_STATUS:
            if service.old_overall_status in (service.ERROR_STATUS, service.ERROR_STATUS):
                alert = False  # Don't alert repeatedly for ERROR
        if service.overall_status == service.PASSING_STATUS:
            if service.old_overall_status == service.WARNING_STATUS:
                alert = False  # Don't alert for recovery from WARNING status

        c = Context({
            'service': service,
            'users': telegram_aliases,
            'host': settings.WWW_HTTP_HOST,
            'scheme': settings.WWW_SCHEME,
            'alert': alert,
            'jenkins_api': settings.JENKINS_API,
        })
        message = Template(telegram_template).render(c)
        self._send_telegram_alert(message, service)

    def _send_telegram_alert(self, message, service):

        telegram_token = env.get('TELEGRAM_BOT_TOKEN')
        chat_id = env.get('TELEGRAM_CHAT_ID')

        tb = telebot.TeleBot(telegram_token)
        tb.send_message(chat_id, message)


class TelegramAlertUserData(AlertPluginUserData):
    name = "Telegram Plugin"
    telegram_id = models.CharField(max_length=50, blank=True)
