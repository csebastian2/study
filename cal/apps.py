from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CalConfig(AppConfig):
    name = 'cal'
    verbose_name = _("Calendar")
