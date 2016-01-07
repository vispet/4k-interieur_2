"""
Celery application
"""

from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from django.conf import settings  # noqa

# pylint: disable=invalid-name
broker_url = settings.BROKER_URL if hasattr(settings, "BROKER_URL") else None
app = Celery("%s-celery" % os.getenv("RACKSPACE_CDN_CONTAINER_PREFIX",
                                     "unknown"),
             broker=broker_url)
# pylint: enable=invalid-name

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
