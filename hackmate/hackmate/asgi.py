__all__ = ()

import os

import django.core.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hackmate.settings")

application = django.core.asgi.get_asgi_application()
