from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StatusConfig(AppConfig):
    name = 'melete.status'
    verbose_name = _("Status")

    def ready(self):
        try:
            import melete.core.signals  # noqa F401
        except ImportError:
            pass
