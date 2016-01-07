"""
WSGI config for project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import newrelic.agent
from django.core.wsgi import get_wsgi_application

# Initialize new relic
# pylint: disable=invalid-name
config_file = os.path.abspath(os.environ.get("NEW_RELIC_CONFIG_FILE"))
environment = os.environ.get("NEW_RELIC_ENVIRONMENT")
# pylint: enable=invalid-name

newrelic.agent.initialize(config_file, environment)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
application = get_wsgi_application()  # pylint: disable=invalid-name
